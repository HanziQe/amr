#!/usr/bin/env python3
"""
Complete demonstration of the AGV Email Agent

This script demonstrates the complete workflow from data loading
to email generation, showing all key features.
"""

from email_agent import EmailAgent
import json


def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 80)
    print(f"  {text}")
    print("=" * 80 + "\n")


def main():
    print_header("AGV Email Agent - Complete Demonstration")
    
    # Step 1: Create the agent
    print("Step 1: Creating Email Agent...")
    agent = EmailAgent()
    print("✓ Agent created with default configuration")
    
    # Step 2: Load the data
    print_header("Step 2: Loading AGV Data")
    data = agent.load_agv_data('cerven.json')
    print(f"✓ Loaded {len(data)} events from cerven.json")
    
    # Show a sample event
    print("\nSample event:")
    sample = data[0]
    for key, value in sample.items():
        print(f"  {key}: {value}")
    
    # Step 3: Analyze the data
    print_header("Step 3: Analyzing Data")
    analysis = agent.analyze_data(data)
    
    print("Summary Statistics:")
    print(f"  • Total Events: {analysis['total_events']}")
    print(f"  • Cleared Events: {analysis['cleared_events']} ({analysis['cleared_events']/analysis['total_events']*100:.1f}%)")
    print(f"  • Active Issues: {analysis['not_cleared_events']} ({analysis['not_cleared_events']/analysis['total_events']*100:.1f}%)")
    print(f"\n  • Date Range: {analysis['date_range']['start']}")
    print(f"                to {analysis['date_range']['end']}")
    print(f"\n  • Components: {', '.join(analysis['components'])}")
    
    print("\nTop 5 Most Common Issues:")
    for i, (issue, count) in enumerate(analysis['top_issues'][:5], 1):
        print(f"  {i}. {issue}: {count} occurrences")
    
    # Step 4: Generate email in Czech
    print_header("Step 4: Generating Czech Email Report")
    body_cs = agent.generate_email_body(analysis, language='cs')
    print(f"✓ Generated Czech email report ({len(body_cs):,} characters)")
    print("  Contains: Summary table, top issues, components, and active issues list")
    
    # Step 5: Generate email in English
    print_header("Step 5: Generating English Email Report")
    body_en = agent.generate_email_body(analysis, language='en')
    print(f"✓ Generated English email report ({len(body_en):,} characters)")
    print("  Contains: Summary table, top issues, components, and active issues list")
    
    # Step 6: Demonstrate sending (dry run)
    print_header("Step 6: Sending Email (Dry Run)")
    print("Demonstrating email sending in dry-run mode...")
    print("(No actual email is sent, just a preview)\n")
    
    success = agent.send_email(
        recipient='manager@example.com',
        subject='AGV System Report - Weekly Summary',
        body=body_cs,
        dry_run=True
    )
    
    if success:
        print("\n✓ Email preview successful!")
    
    # Step 7: Complete workflow
    print_header("Step 7: Complete Workflow (One Command)")
    print("The agent can do all of the above in a single call:")
    print("\n  agent.generate_and_send_report(")
    print("      json_file='cerven.json',")
    print("      recipient='manager@example.com',")
    print("      language='cs',")
    print("      dry_run=True")
    print("  )")
    
    # Step 8: Configuration
    print_header("Step 8: Custom Configuration")
    print("For production use, configure SMTP settings:")
    print("\n1. Copy config_example.json to config.json")
    print("2. Edit with your SMTP credentials")
    print("3. Load configuration:")
    print("\n   with open('config.json', 'r') as f:")
    print("       config = json.load(f)")
    print("   agent = EmailAgent(config)")
    print("\n4. Set dry_run=False to send real emails")
    
    # Summary
    print_header("Summary")
    print("The AGV Email Agent provides:")
    print("  ✓ Automatic data analysis of AGV event logs")
    print("  ✓ Professional HTML email reports")
    print("  ✓ Bilingual support (Czech and English)")
    print("  ✓ Safe testing with dry-run mode")
    print("  ✓ Flexible configuration")
    print("  ✓ Easy integration into your workflow")
    
    print("\n" + "=" * 80)
    print("For more information, see README.md")
    print("For usage examples, run: python example_usage.py")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
