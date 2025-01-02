# Business Email Automation

An AI-powered system for finding businesses without websites and automatically sending personalized outreach emails.

## Features

- **Lead Finding**
  - Google Places API integration
  - Yelp API integration
  - Foursquare API integration
  - Website existence verification
  - Duplicate lead detection

- **Email Automation**
  - SendGrid integration for reliable email delivery
  - Personalized email templates
  - Automated scheduling
  - Email tracking
  - Anti-spam compliance
  - Unsubscribe handling

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/business-email-automation.git
cd business-email-automation
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file:
```bash
cp .env.example .env
```

4. Add your API keys and configuration to `.env`:
- Google Places API key
- Yelp API key
- Foursquare API key
- SendGrid API key
- Your business information

## Usage

### Running the System

1. Start the automated system:
```bash
python src/main.py
```

This will:
- Find new leads daily at 9 AM
- Send emails to new leads daily at 10 AM

### Manual Operation

You can also run individual components:

```python
from src.lead_finder import LeadFinder
from src.email_sender import EmailSender

# Find leads
finder = LeadFinder()
leads = finder.find_all_leads("Atlanta, GA")

# Send emails
sender = EmailSender()
sender.send_email("business@example.com", lead_data)
```

## Configuration

### Lead Finding
- Adjust search radius in `lead_finder.py`
- Modify location targeting
- Add additional data sources

### Email Templates
- Customize email templates in `email_sender.py`
- Add multiple template variations
- Implement A/B testing

## Compliance

This system includes:
- Unsubscribe mechanism
- Rate limiting
- Email sending delays
- GDPR compliance features

## Monitoring

The system logs:
- New leads found
- Emails sent
- Success/failure rates
- API usage

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
