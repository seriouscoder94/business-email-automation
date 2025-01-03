from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
from dotenv import load_dotenv
import json

load_dotenv()

# Get credentials from environment
api_key = os.getenv('SENDGRID_API_KEY')
from_email = os.getenv('SENDER_EMAIL')
sender_name = os.getenv('SENDER_NAME')
company_name = os.getenv('COMPANY_NAME')

print("Environment variables loaded:")
print(f"From Email: {from_email}")
print(f"Sender Name: {sender_name}")
print(f"Company: {company_name}")

# Test business details
business_name = "Test Coffee Shop"
business_type = "cafe"
location = "Atlanta, GA"

# Load template
template_path = 'src/data/templates/business_template.json'
print(f"\nLoading template from: {template_path}")

try:
    with open(template_path, 'r') as f:
        template = json.load(f)
except Exception as e:
    print(f"Error loading template: {str(e)}")
    exit(1)

print("Template loaded successfully")

# Replace placeholders
subject = template['subject'].replace('{{business_name}}', business_name)
content = template['content']
content = content.replace('{{business_name}}', business_name)
content = content.replace('{{business_type}}', business_type)
content = content.replace('{{location}}', location)
content = content.replace('{{sender_name}}', sender_name)
content = content.replace('{{company_name}}', company_name)

print("\nEmail Details:")
print(f"From: {sender_name} <{from_email}>")
print(f"To: webreachconnect@gmail.com")
print(f"Subject: {subject}")
print("\nContent Preview:")
print("-------------------")
print(content[:200] + "...")
print("-------------------")

# Create test message
message = Mail(
    from_email=(from_email, sender_name),
    to_emails='webreachconnect@gmail.com',
    subject=subject,
    html_content=content.replace('\n', '<br>')
)

try:
    # Initialize SendGrid client
    print("\nInitializing SendGrid client...")
    sg = SendGridAPIClient(api_key)
    
    # Send email
    print("Sending email...")
    response = sg.send(message)
    
    # Print response details
    print(f"\nResponse Status Code: {response.status_code}")
    print(f"Response Headers: {response.headers}")
    
    if response.status_code == 202:
        print("\nBusiness template test sent successfully!")
        print("Check your Gmail inbox (and spam folder) to review how it looks")
    else:
        print(f"\nUnexpected status code: {response.status_code}")
        
except Exception as e:
    print(f"\nError sending email: {str(e)}")
    print(f"Error details: {e.args}")
