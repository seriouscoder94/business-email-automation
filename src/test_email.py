from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# SendGrid configuration
api_key = os.getenv('SENDGRID_API_KEY')
sender_email = os.getenv('SENDER_EMAIL')
sender_name = os.getenv('SENDER_NAME')
reply_to = 'webreachconnect@gmail.com'

print(f"\nEmail Configuration:")
print(f"API Key (first 10 chars): {api_key[:10]}...")
print(f"Sender Email: {sender_email}")
print(f"Sender Name: {sender_name}")
print(f"Reply To: {reply_to}")

# Create test message
message = Mail(
    from_email=sender_email,
    to_emails='dailywork813@gmail.com',
    subject='Test Email from Web Reach Connect',
    plain_text_content='This is a test email to verify SendGrid integration is working correctly.'
)

# Add reply-to
message.reply_to = Email(reply_to)

try:
    # Send email
    sg = SendGridAPIClient(api_key)
    response = sg.send(message)
    
    print(f"\nSendGrid Response:")
    print(f"Status Code: {response.status_code}")
    print(f"Body: {response.body}")
    print(f"Headers: {response.headers}")
    
except Exception as e:
    print(f"\nError sending email:")
    print(f"Type: {type(e).__name__}")
    print(f"Message: {str(e)}")
    if hasattr(e, 'body'):
        print(f"Body: {e.body}")
