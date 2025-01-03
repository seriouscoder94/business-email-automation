from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
from dotenv import load_dotenv

load_dotenv()

# Get API key and email from environment
api_key = os.getenv('SENDGRID_API_KEY')
from_email = os.getenv('SENDER_EMAIL')

print(f"Using API key: {api_key[:20]}...")
print(f"Sending from: {from_email}")

# Create the email
message = Mail(
    from_email=from_email,
    to_emails=from_email,
    subject='Simple Test Email',
    html_content='This is a test email to verify SendGrid is working.')

try:
    # Initialize SendGrid client
    sg = SendGridAPIClient(api_key)
    
    # Send the email
    response = sg.send(message)
    
    # Print response details
    print(f"Status code: {response.status_code}")
    print(f"Response headers: {response.headers}")
    print("Email sent successfully!")
    
except Exception as e:
    print(f"Error sending email: {str(e)}")
