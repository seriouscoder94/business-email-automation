# Business Email Automation System

A powerful email automation system built with Flask and SendGrid for managing business leads and sending personalized emails.

## Features

- Send personalized emails using templates
- Lead management system
- Email template management
- Campaign tracking
- Support for reply-to addresses
- Detailed logging for troubleshooting

## Prerequisites

- Python 3.8+
- SendGrid API key with Mail Send permissions
- Verified sender email in SendGrid

## Environment Variables

Create a `.env` file with the following variables:

```env
SENDGRID_API_KEY=your_sendgrid_api_key
SENDER_EMAIL=your_verified_sender_email
SENDER_NAME=Your Name
COMPANY_NAME=Your Company
REPLY_TO_EMAIL=your_reply_to_email
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/business_email_automation.git
cd business_email_automation
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your environment variables in `.env`

4. Run the application:
```bash
python src/app.py
```

The application will be available at http://localhost:5003

## Project Structure

```
business_email_automation/
├── src/
│   ├── app.py              # Main Flask application
│   ├── email_sender.py     # Email sending functionality
│   ├── lead_finder.py      # Lead management
│   ├── campaign_handler.py # Campaign management
│   ├── templates/          # HTML templates
│   └── static/             # Static files
├── data/
│   ├── leads.json         # Lead storage
│   ├── templates/         # Email templates
│   └── campaigns/         # Campaign data
└── README.md
```

## Usage

1. Add leads through the web interface
2. Create email templates with personalization variables
3. Send personalized emails to leads
4. Track email campaigns and lead status

## Security Notes

- Never commit your `.env` file
- Keep your SendGrid API key secure
- Use environment variables for sensitive data
- Regularly rotate API keys

## Author

Oscar Hernandez

## License

This project is licensed under the MIT License - see the LICENSE file for details
