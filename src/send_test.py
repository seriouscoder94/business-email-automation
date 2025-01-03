from email_sender import EmailSender
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Create a test lead
test_lead = {
    'id': 'test_1',
    'business_name': 'Test Coffee Shop',
    'business_type': 'cafe',
    'location': 'Atlanta, GA',
    'email': os.getenv('SENDER_EMAIL')  # Sending to yourself
}

# Initialize email sender
email_sender = EmailSender()

# Load the template
with open('src/data/templates/business_template.json', 'r') as f:
    template = json.load(f)

# Create and process test campaign
campaign_id = email_sender.create_campaign(
    name='Template Test',
    template_id='business_template',
    leads=[test_lead]
)

print("\nSending test email...")
email_sender.process_campaigns()
print(f"\nTest email sent to {test_lead['email']}")
print("Check your inbox (including spam folder) to review the template!")
