#!/usr/bin/env python3
"""
Save sample email output to HTML file for demonstration
"""

from email_agent import EmailAgent

# Create agent
agent = EmailAgent()

# Load and analyze data
data = agent.load_agv_data('cerven.json')
analysis = agent.analyze_data(data)

# Generate both Czech and English versions
body_cs = agent.generate_email_body(analysis, language='cs')
body_en = agent.generate_email_body(analysis, language='en')

# Save to files
with open('sample_email_cs.html', 'w', encoding='utf-8') as f:
    f.write(body_cs)
print("Czech sample saved to sample_email_cs.html")

with open('sample_email_en.html', 'w', encoding='utf-8') as f:
    f.write(body_en)
print("English sample saved to sample_email_en.html")

print("\nYou can open these files in a web browser to see how the emails will look.")
