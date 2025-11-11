#!/usr/bin/env python3
"""
Email Agent for AGV Data Analysis and Reporting
Analyzes AGV (Automated Guided Vehicle) data and generates email reports
"""

import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import Dict, List, Any
from collections import Counter


class EmailAgent:
    """Agent for analyzing AGV data and sending email reports"""
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize the Email Agent
        
        Args:
            config: Configuration dictionary with SMTP settings
        """
        self.config = config or {}
        self.smtp_server = self.config.get('smtp_server', 'localhost')
        self.smtp_port = self.config.get('smtp_port', 587)
        self.sender_email = self.config.get('sender_email', 'agv-agent@example.com')
        self.sender_password = self.config.get('sender_password', '')
        self.use_tls = self.config.get('use_tls', True)
    
    def load_agv_data(self, json_file: str) -> List[Dict[str, Any]]:
        """
        Load AGV data from JSON file
        
        Args:
            json_file: Path to JSON file containing AGV data
            
        Returns:
            List of AGV event dictionaries
        """
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    
    def analyze_data(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze AGV data and generate statistics
        
        Args:
            data: List of AGV event dictionaries
            
        Returns:
            Dictionary containing analysis results
        """
        # Count events by type
        event_titles = [event.get('Title', 'Unknown') for event in data]
        event_counts = Counter(event_titles)
        
        # Count cleared vs non-cleared events
        cleared_count = sum(1 for event in data if event.get('Cleared'))
        not_cleared_count = sum(1 for event in data if not event.get('Cleared'))
        
        # Get date range
        timestamps = [event.get('TimeStamp', '') for event in data if event.get('TimeStamp')]
        date_range = {
            'start': min(timestamps) if timestamps else 'N/A',
            'end': max(timestamps) if timestamps else 'N/A'
        }
        
        # Get components
        components = set(event.get('ComponentName', 'Unknown') for event in data)
        
        # Find most common issues
        top_issues = event_counts.most_common(10)
        
        # Count active (not cleared) issues
        active_issues = [event for event in data if not event.get('Cleared')]
        
        return {
            'total_events': len(data),
            'cleared_events': cleared_count,
            'not_cleared_events': not_cleared_count,
            'date_range': date_range,
            'components': list(components),
            'top_issues': top_issues,
            'active_issues': active_issues,
            'event_counts': event_counts
        }
    
    def generate_email_body(self, analysis: Dict[str, Any], language: str = 'en') -> str:
        """
        Generate email body from analysis results
        
        Args:
            analysis: Analysis results dictionary
            language: Language for the email ('en' or 'cs' for Czech)
            
        Returns:
            HTML email body
        """
        if language == 'cs':
            return self._generate_czech_email(analysis)
        else:
            return self._generate_english_email(analysis)
    
    def _generate_english_email(self, analysis: Dict[str, Any]) -> str:
        """Generate email body in English"""
        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
                h1 {{ color: #2c3e50; }}
                h2 {{ color: #34495e; }}
                table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
                th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
                th {{ background-color: #3498db; color: white; }}
                tr:nth-child(even) {{ background-color: #f2f2f2; }}
                .warning {{ color: #e74c3c; font-weight: bold; }}
                .success {{ color: #27ae60; font-weight: bold; }}
            </style>
        </head>
        <body>
            <h1>AGV System Report</h1>
            <p><strong>Report Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            
            <h2>Summary</h2>
            <table>
                <tr>
                    <th>Metric</th>
                    <th>Value</th>
                </tr>
                <tr>
                    <td>Total Events</td>
                    <td>{analysis['total_events']}</td>
                </tr>
                <tr>
                    <td>Cleared Events</td>
                    <td class="success">{analysis['cleared_events']}</td>
                </tr>
                <tr>
                    <td>Active Issues</td>
                    <td class="warning">{analysis['not_cleared_events']}</td>
                </tr>
                <tr>
                    <td>Date Range</td>
                    <td>{analysis['date_range']['start']} to {analysis['date_range']['end']}</td>
                </tr>
            </table>
            
            <h2>Top 10 Most Common Issues</h2>
            <table>
                <tr>
                    <th>Issue Type</th>
                    <th>Count</th>
                </tr>
        """
        
        for issue, count in analysis['top_issues']:
            html += f"""
                <tr>
                    <td>{issue}</td>
                    <td>{count}</td>
                </tr>
            """
        
        html += """
            </table>
            
            <h2>Components Involved</h2>
            <ul>
        """
        
        for component in analysis['components']:
            html += f"<li>{component}</li>"
        
        html += """
            </ul>
        """
        
        # Add active issues if any
        if analysis['active_issues']:
            html += f"""
            <h2 class="warning">Active Issues ({len(analysis['active_issues'])})</h2>
            <p>The following issues are currently not cleared:</p>
            <table>
                <tr>
                    <th>Timestamp</th>
                    <th>Issue</th>
                    <th>Component</th>
                </tr>
            """
            
            # Show first 20 active issues
            for issue in analysis['active_issues'][:20]:
                html += f"""
                <tr>
                    <td>{issue.get('TimeStamp', 'N/A')}</td>
                    <td>{issue.get('Title', 'Unknown')}</td>
                    <td>{issue.get('ComponentName', 'Unknown')}</td>
                </tr>
                """
            
            if len(analysis['active_issues']) > 20:
                html += f"""
                <tr>
                    <td colspan="3"><em>... and {len(analysis['active_issues']) - 20} more</em></td>
                </tr>
                """
            
            html += """
            </table>
            """
        
        html += """
        </body>
        </html>
        """
        
        return html
    
    def _generate_czech_email(self, analysis: Dict[str, Any]) -> str:
        """Generate email body in Czech"""
        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
                h1 {{ color: #2c3e50; }}
                h2 {{ color: #34495e; }}
                table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
                th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
                th {{ background-color: #3498db; color: white; }}
                tr:nth-child(even) {{ background-color: #f2f2f2; }}
                .warning {{ color: #e74c3c; font-weight: bold; }}
                .success {{ color: #27ae60; font-weight: bold; }}
            </style>
        </head>
        <body>
            <h1>Zpráva o systému AGV</h1>
            <p><strong>Zpráva vygenerována:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            
            <h2>Souhrn</h2>
            <table>
                <tr>
                    <th>Metrika</th>
                    <th>Hodnota</th>
                </tr>
                <tr>
                    <td>Celkem událostí</td>
                    <td>{analysis['total_events']}</td>
                </tr>
                <tr>
                    <td>Vyřešené události</td>
                    <td class="success">{analysis['cleared_events']}</td>
                </tr>
                <tr>
                    <td>Aktivní problémy</td>
                    <td class="warning">{analysis['not_cleared_events']}</td>
                </tr>
                <tr>
                    <td>Časové období</td>
                    <td>{analysis['date_range']['start']} až {analysis['date_range']['end']}</td>
                </tr>
            </table>
            
            <h2>10 nejčastějších problémů</h2>
            <table>
                <tr>
                    <th>Typ problému</th>
                    <th>Počet</th>
                </tr>
        """
        
        for issue, count in analysis['top_issues']:
            html += f"""
                <tr>
                    <td>{issue}</td>
                    <td>{count}</td>
                </tr>
            """
        
        html += """
            </table>
            
            <h2>Zapojené komponenty</h2>
            <ul>
        """
        
        for component in analysis['components']:
            html += f"<li>{component}</li>"
        
        html += """
            </ul>
        """
        
        # Add active issues if any
        if analysis['active_issues']:
            html += f"""
            <h2 class="warning">Aktivní problémy ({len(analysis['active_issues'])})</h2>
            <p>Následující problémy nejsou vyřešeny:</p>
            <table>
                <tr>
                    <th>Časové razítko</th>
                    <th>Problém</th>
                    <th>Komponenta</th>
                </tr>
            """
            
            # Show first 20 active issues
            for issue in analysis['active_issues'][:20]:
                html += f"""
                <tr>
                    <td>{issue.get('TimeStamp', 'N/A')}</td>
                    <td>{issue.get('Title', 'Neznámý')}</td>
                    <td>{issue.get('ComponentName', 'Neznámý')}</td>
                </tr>
                """
            
            if len(analysis['active_issues']) > 20:
                html += f"""
                <tr>
                    <td colspan="3"><em>... a dalších {len(analysis['active_issues']) - 20}</em></td>
                </tr>
                """
            
            html += """
            </table>
            """
        
        html += """
        </body>
        </html>
        """
        
        return html
    
    def send_email(self, recipient: str, subject: str, body: str, dry_run: bool = True) -> bool:
        """
        Send email report
        
        Args:
            recipient: Email address of recipient
            subject: Email subject
            body: HTML body of email
            dry_run: If True, only print email without sending
            
        Returns:
            True if successful, False otherwise
        """
        if dry_run:
            print("=" * 80)
            print("DRY RUN - Email would be sent with the following details:")
            print(f"From: {self.sender_email}")
            print(f"To: {recipient}")
            print(f"Subject: {subject}")
            print("=" * 80)
            print("Body preview (first 500 chars):")
            print(body[:500] + "..." if len(body) > 500 else body)
            print("=" * 80)
            return True
        
        try:
            # Create message
            message = MIMEMultipart('alternative')
            message['Subject'] = subject
            message['From'] = self.sender_email
            message['To'] = recipient
            
            # Attach HTML body
            html_part = MIMEText(body, 'html')
            message.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                if self.use_tls:
                    server.starttls()
                if self.sender_password:
                    server.login(self.sender_email, self.sender_password)
                server.send_message(message)
            
            print(f"Email sent successfully to {recipient}")
            return True
            
        except Exception as e:
            print(f"Failed to send email: {str(e)}")
            return False
    
    def generate_and_send_report(self, 
                                 json_file: str, 
                                 recipient: str, 
                                 language: str = 'en',
                                 dry_run: bool = True) -> bool:
        """
        Complete workflow: load data, analyze, generate email, and send
        
        Args:
            json_file: Path to JSON file with AGV data
            recipient: Email recipient
            language: Language for report ('en' or 'cs')
            dry_run: If True, only preview without sending
            
        Returns:
            True if successful, False otherwise
        """
        print(f"Loading data from {json_file}...")
        data = self.load_agv_data(json_file)
        
        print(f"Analyzing {len(data)} events...")
        analysis = self.analyze_data(data)
        
        print(f"Generating email in {language}...")
        body = self.generate_email_body(analysis, language)
        
        subject = "AGV System Report" if language == 'en' else "Zpráva o systému AGV"
        subject += f" - {datetime.now().strftime('%Y-%m-%d')}"
        
        print(f"Sending email to {recipient}...")
        return self.send_email(recipient, subject, body, dry_run)


if __name__ == "__main__":
    import sys
    
    # Simple command-line interface
    if len(sys.argv) < 2:
        print("Usage: python email_agent.py <json_file> [recipient] [language]")
        print("Example: python email_agent.py cerven.json admin@example.com cs")
        sys.exit(1)
    
    json_file = sys.argv[1]
    recipient = sys.argv[2] if len(sys.argv) > 2 else "admin@example.com"
    language = sys.argv[3] if len(sys.argv) > 3 else "en"
    
    # Create agent with default config (dry run mode)
    agent = EmailAgent()
    
    # Generate and send report
    success = agent.generate_and_send_report(
        json_file=json_file,
        recipient=recipient,
        language=language,
        dry_run=True  # Set to False to actually send emails
    )
    
    sys.exit(0 if success else 1)
