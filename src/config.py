import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
env_path = Path(__file__).parent / '.env'
load_dotenv(env_path)

class Config:
    """Application configuration class"""
    
    # Server settings
    PORT = int(os.getenv('PORT', 5008))
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    
    # API Keys
    GOOGLE_PLACES_API_KEY = os.getenv('GOOGLE_PLACES_API_KEY')
    YELP_API_KEY = os.getenv('YELP_API_KEY')
    SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
    
    # Test API Keys (for development)
    TEST_GOOGLE_PLACES_API_KEY = os.getenv('TEST_GOOGLE_PLACES_API_KEY')
    TEST_YELP_API_KEY = os.getenv('TEST_YELP_API_KEY')
    
    @classmethod
    def get_google_api_key(cls):
        """Get Google Places API key with fallback to test key"""
        return cls.GOOGLE_PLACES_API_KEY or cls.TEST_GOOGLE_PLACES_API_KEY
    
    @classmethod
    def get_yelp_api_key(cls):
        """Get Yelp API key with fallback to test key"""
        return cls.YELP_API_KEY or cls.TEST_YELP_API_KEY
    
    @classmethod
    def validate_config(cls):
        """Validate configuration and return list of missing required settings"""
        missing = []
        
        if not cls.get_google_api_key():
            missing.append('Google Places API Key')
        if not cls.get_yelp_api_key():
            missing.append('Yelp API Key')
        if not cls.SENDGRID_API_KEY:
            missing.append('SendGrid API Key')
            
        return missing
    
    @classmethod
    def is_development(cls):
        """Check if running in development mode"""
        return cls.DEBUG
    
    @classmethod
    def log_config_status(cls):
        """Log configuration status"""
        missing = cls.validate_config()
        
        if missing:
            print("⚠️ WARNING: Missing required configuration:")
            for item in missing:
                print(f"  - {item}")
        else:
            print("✅ All required configuration is present")
            
        if cls.is_development():
            print("🔧 Running in DEVELOPMENT mode")
            if cls.TEST_GOOGLE_PLACES_API_KEY:
                print("  - Using TEST Google Places API Key")
            if cls.TEST_YELP_API_KEY:
                print("  - Using TEST Yelp API Key")
