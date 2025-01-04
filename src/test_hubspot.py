import os
from dotenv import load_dotenv
from crm_integration import CRMIntegration

def test_hubspot_connection():
    # Load environment variables
    load_dotenv()
    
    # Initialize CRM integration
    crm = CRMIntegration()
    
    # Test data
    test_business = {
        'name': 'Test Business',
        'email': 'test@example.com',
        'phone': '555-0123',
        'address': '123 Test St, Atlanta, GA',
        'industry': 'Technology'
    }
    
    try:
        # Try to create a contact
        contact_ids = crm.export_to_hubspot([test_business])
        if contact_ids:
            print(f"✅ Successfully connected to HubSpot!")
            print(f"Created test contact with ID: {contact_ids[0]}")
            return True
    except Exception as e:
        print(f"❌ Error connecting to HubSpot: {str(e)}")
        return False

if __name__ == "__main__":
    test_hubspot_connection()
