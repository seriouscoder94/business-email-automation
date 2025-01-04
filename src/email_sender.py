"""
Email Sender Module for Business Email Automation

This module handles all email-related functionality using SendGrid API.
It manages email templates, sending emails to leads, and handling email campaigns.

Key Features:
- Send personalized emails using templates
- Support for reply-to email addresses
- Detailed logging of email sending process
- Error handling and status reporting

Dependencies:
- SendGrid API for email delivery
- python-dotenv for environment variable management

Environment Variables Required:
- SENDGRID_API_KEY: Your SendGrid API key
- SENDER_EMAIL: Verified sender email address
- SENDER_NAME: Name to appear as the sender
- COMPANY_NAME: Your company name

Author: Oscar Hernandez
Date: January 2025
"""

import json
import os
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from business_discovery import BusinessDiscoveryEngine

load_dotenv()

app = Flask(__name__)

class EmailSender:
    def __init__(self):
        self.api_key = os.environ.get('SENDGRID_API_KEY')
        if not self.api_key:
            raise ValueError("SENDGRID_API_KEY not found in environment variables")
        self.sg = SendGridAPIClient(self.api_key)
        self.from_email = Email('sam@webreachconnect.com', 'Sam from Web Reach Connect')

    def send_email(self, to_email, subject, content):
        """
        Send an email using SendGrid.
        
        Args:
            to_email (str): Recipient's email address
            subject (str): Email subject
            content (str): Email content (plain text)
            
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            print(f"Attempting to send email to {to_email}")
            print(f"Subject: {subject}")
            print(f"Content: {content}")
            
            # Create message
            message = Mail(
                from_email=self.from_email,
                to_emails=to_email,
                subject=subject,
                plain_text_content=content
            )
            
            # Convert the Mail object to a SendGrid-formatted dictionary
            message_dict = message.get()
            
            # Send email using the SendGrid client
            response = self.sg.client.mail.send.post(request_body=message_dict)
            
            print(f"SendGrid Response Status Code: {response.status_code}")
            print(f"SendGrid Response Headers: {response.headers}")
            
            if response.status_code in [200, 201, 202]:
                print("Email sent successfully!")
                return True, "Email sent successfully"
            else:
                error_msg = f"SendGrid error: Status {response.status_code}"
                print(error_msg)
                return False, error_msg
            
        except Exception as e:
            error_msg = f"Failed to send email: {str(e)}"
            print(f"Error details: {error_msg}")
            return False, error_msg

    def send_direct_email(self, to_email, subject, content, from_email=None, from_name=None):
        try:
            message = Mail(
                from_email=from_email or self.from_email,
                to_emails=to_email,
                subject=subject,
                plain_text_content=content
            )
            
            response = self.sg.send(message)
            print(f"Direct email sent to {to_email} with status code: {response.status_code}")
            return True, "Email sent successfully"
            
        except Exception as e:
            error_msg = f"Failed to send direct email: {str(e)}"
            print(error_msg)
            return False, error_msg

@app.route('/leads')
def lead_generation():
    return render_template('lead_generation.html')

@app.route('/ai-agent')
def ai_agent():
    return render_template('ai_agent.html')

@app.route('/api/search-businesses')
def search_businesses():
    business_type = request.args.get('type', '')
    location = request.args.get('location', '')
    radius = int(request.args.get('radius', '10'))

    # TODO: Integrate with Google Places or Yelp API
    # For now, using mock data
    mock_businesses = [
        {
            "name": "Sample Restaurant",
            "type": "restaurant",
            "address": "123 Main St, " + location,
            "phone": "(555) 123-4567",
            "website": "",  # Empty website indicates a potential lead
            "email": "",
            "hasWebsite": False
        },
        {
            "name": "Local Salon",
            "type": "salon",
            "address": "456 Oak Ave, " + location,
            "phone": "(555) 987-6543",
            "website": "",
            "email": "",
            "hasWebsite": False
        },
        {
            "name": "Downtown Retail",
            "type": "retail",
            "address": "789 Market St, " + location,
            "phone": "(555) 456-7890",
            "website": "",
            "email": "",
            "hasWebsite": False
        }
    ]

    # Filter by business type if specified
    if business_type:
        mock_businesses = [b for b in mock_businesses if b['type'] == business_type]

    # In the real implementation, we would:
    # 1. Search for businesses using Google Places/Yelp API
    # 2. Filter out businesses that have websites
    # 3. Format the response to match our needs

    return jsonify({"businesses": mock_businesses})

@app.route('/api/discover-businesses', methods=['POST'])
async def discover_businesses():
    data = request.get_json()
    region = data.get('location', '')
    industry = data.get('business_type', '')
    keywords = data.get('keywords', [])

    if not region or not industry:
        return jsonify({'error': 'Location and business type are required'}), 400

    engine = BusinessDiscoveryEngine()
    try:
        businesses = await engine.discover_businesses(region, industry, keywords)
        return jsonify({
            'success': True,
            'businesses': [vars(b) for b in businesses],
            'total': len(businesses)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
