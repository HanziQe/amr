#!/usr/bin/env python3
"""
Example usage of the Email Agent for AGV data reporting
"""

import json
from email_agent import EmailAgent


def example_basic_usage():
    """Basic example: Load data and generate report"""
    print("=" * 80)
    print("Example 1: Basic Usage")
    print("=" * 80)
    
    # Create email agent
    agent = EmailAgent()
    
    # Generate report from the cerven.json file
    agent.generate_and_send_report(
        json_file='cerven.json',
        recipient='manager@example.com',
        language='cs',  # Czech language
        dry_run=True  # Preview only, don't actually send
    )


def example_with_custom_config():
    """Example with custom SMTP configuration"""
    print("\n" + "=" * 80)
    print("Example 2: With Custom Configuration")
    print("=" * 80)
    
    # Load configuration from file
    with open('config_example.json', 'r') as f:
        config = json.load(f)
    
    # Create agent with custom config
    agent = EmailAgent(config)
    
    # Generate report in English
    agent.generate_and_send_report(
        json_file='cerven.json',
        recipient='admin@example.com',
        language='en',
        dry_run=True
    )


def example_custom_analysis():
    """Example: Load data, analyze, and create custom report"""
    print("\n" + "=" * 80)
    print("Example 3: Custom Analysis")
    print("=" * 80)
    
    agent = EmailAgent()
    
    # Load and analyze data
    data = agent.load_agv_data('cerven.json')
    analysis = agent.analyze_data(data)
    
    # Print some statistics
    print(f"\nTotal Events: {analysis['total_events']}")
    print(f"Cleared Events: {analysis['cleared_events']}")
    print(f"Active Issues: {analysis['not_cleared_events']}")
    print(f"\nDate Range: {analysis['date_range']['start']} to {analysis['date_range']['end']}")
    print(f"\nComponents: {', '.join(analysis['components'])}")
    
    print("\nTop 5 Issues:")
    for i, (issue, count) in enumerate(analysis['top_issues'][:5], 1):
        print(f"{i}. {issue}: {count} times")
    
    # Generate email body
    body = agent.generate_email_body(analysis, language='cs')
    
    # Send (dry run)
    agent.send_email(
        recipient='operations@example.com',
        subject='AGV Custom Report',
        body=body,
        dry_run=True
    )


def example_multiple_recipients():
    """Example: Send report to multiple recipients"""
    print("\n" + "=" * 80)
    print("Example 4: Multiple Recipients")
    print("=" * 80)
    
    agent = EmailAgent()
    recipients = [
        'manager@example.com',
        'technician@example.com',
        'supervisor@example.com'
    ]
    
    # Load and analyze once
    data = agent.load_agv_data('cerven.json')
    analysis = agent.analyze_data(data)
    
    # Generate email body
    body_cs = agent.generate_email_body(analysis, language='cs')
    
    # Send to all recipients
    for recipient in recipients:
        print(f"\nSending to {recipient}...")
        agent.send_email(
            recipient=recipient,
            subject=f"AGV Report - {analysis['date_range']['start']}",
            body=body_cs,
            dry_run=True
        )


if __name__ == "__main__":
    print("\n")
    print("*" * 80)
    print("AGV Email Agent - Usage Examples")
    print("*" * 80)
    
    # Run all examples
    example_basic_usage()
    example_with_custom_config()
    example_custom_analysis()
    example_multiple_recipients()
    
    print("\n" + "=" * 80)
    print("All examples completed!")
    print("=" * 80)
    print("\nTo actually send emails:")
    print("1. Edit config_example.json with your SMTP settings")
    print("2. Change dry_run=False in the examples")
    print("3. Run the script again")
    print("=" * 80)
