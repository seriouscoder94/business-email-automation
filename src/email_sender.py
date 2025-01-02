import os
from typing import Dict
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from dotenv import load_dotenv

load_dotenv()

class EmailSender:
    def __init__(self):
        self.api_key = os.getenv('SENDGRID_API_KEY')
        self.from_email = os.getenv('FROM_EMAIL')
        self.business_name = os.getenv('BUSINESS_NAME')
        self.your_name = os.getenv('YOUR_NAME')
        self.calendar_link = os.getenv('CALENDAR_LINK')
        self.contact_phone = os.getenv('CONTACT_PHONE')
        self.website = os.getenv('WEBSITE')
        
        self.sg = SendGridAPIClient(self.api_key)
        
    def create_email_content(self, lead: Dict) -> tuple:
        """Create personalized email subject and body."""
        business_name = lead['business_name']
        
        subject = f"Boost {business_name}'s Online Presence with a Modern Website"
        
        body = f"""
        Hi,
        
        I noticed that {business_name} doesn't have a website yet. In today's digital age, having a strong online presence is crucial for business growth and customer engagement.
        
        I specialize in creating affordable, modern websites for local businesses like yours. My services include:
        • Professional website design tailored to your business
        • Mobile-friendly layouts
        • Search engine optimization (SEO)
        • Easy content management system
        • Social media integration
        
        I'd love to discuss how I can help {business_name} establish a strong online presence. Would you be interested in a quick 15-minute call to explore the possibilities?
        
        You can schedule a call at your convenience here: {self.calendar_link}
        
        Best regards,
        {self.your_name}
        {self.business_name}
        {self.website}
        {self.contact_phone}
        
        P.S. If you're not the right person to discuss this, I'd greatly appreciate it if you could forward this to the appropriate contact.
        
        To unsubscribe from future emails, simply reply with "unsubscribe" in the subject line.
        """
        
        return subject, body
        
    def send_email(self, to_email: str, lead: Dict) -> bool:
        """Send email using SendGrid."""
        try:
            subject, body = self.create_email_content(lead)
            
            message = Mail(
                from_email=Email(self.from_email),
                to_emails=To(to_email),
                subject=subject,
                plain_text_content=Content("text/plain", body)
            )
            
            response = self.sg.send(message)
            if response.status_code in [200, 201, 202]:
                print(f"Email sent successfully to {to_email}")
                return True
            else:
                print(f"Failed to send email to {to_email}. Status code: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"Error sending email to {to_email}: {str(e)}")
            return False
