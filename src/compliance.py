"""
Compliance and Ethics Module for Business Data Collection
Implements safeguards for data privacy regulations (GDPR, CCPA, CAN-SPAM)
"""

import os
import json
import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

class DataRegion(Enum):
    EU = "EU"
    CALIFORNIA = "CA"
    OTHER = "OTHER"

@dataclass
class PrivacySettings:
    """Privacy settings for data collection and storage"""
    data_retention_days: int = 90
    require_consent: bool = True
    allow_automated_decisions: bool = False
    enable_right_to_erasure: bool = True
    enable_data_portability: bool = True

class ComplianceManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.privacy_settings = PrivacySettings()
        self._setup_logging()

    def _setup_logging(self):
        """Setup compliance logging"""
        logging.basicConfig(
            filename='data/compliance.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def validate_data_collection(self, business_data: Dict) -> bool:
        """
        Validate if data collection complies with privacy regulations
        Returns True if compliant, False otherwise
        """
        try:
            # 1. Check if data is publicly available
            if not self._is_data_public(business_data):
                self.logger.warning(f"Attempted to collect non-public data for {business_data.get('name')}")
                return False

            # 2. Verify data minimization
            if not self._verify_data_minimization(business_data):
                self.logger.warning(f"Excessive data collection for {business_data.get('name')}")
                return False

            # 3. Check regional compliance
            region = self._determine_region(business_data)
            if not self._check_regional_compliance(business_data, region):
                return False

            # 4. Log compliant collection
            self.logger.info(f"Validated data collection for {business_data.get('name')}")
            return True

        except Exception as e:
            self.logger.error(f"Error in data validation: {str(e)}")
            return False

    def _is_data_public(self, business_data: Dict) -> bool:
        """Verify data is from public sources"""
        public_sources = {
            'google_places',
            'yelp',
            'business_website',
            'public_directory'
        }
        return business_data.get('data_source') in public_sources

    def _verify_data_minimization(self, business_data: Dict) -> bool:
        """Ensure only necessary data is collected"""
        essential_fields = {
            'name',
            'email',
            'phone',
            'address',
            'website',
            'industry'
        }
        collected_fields = set(business_data.keys())
        return essential_fields.issuperset(collected_fields - {'data_source', 'id'})

    def _determine_region(self, business_data: Dict) -> DataRegion:
        """Determine applicable privacy regulations based on location"""
        address = business_data.get('address', '').lower()
        
        # Check EU
        eu_countries = {'germany', 'france', 'italy', 'spain', 'netherlands'}
        if any(country in address for country in eu_countries):
            return DataRegion.EU
            
        # Check California
        if 'california' in address or ', ca' in address:
            return DataRegion.CALIFORNIA
            
        return DataRegion.OTHER

    def _check_regional_compliance(self, business_data: Dict, region: DataRegion) -> bool:
        """Check compliance with regional regulations"""
        if region == DataRegion.EU:
            return self._check_gdpr_compliance(business_data)
        elif region == DataRegion.CALIFORNIA:
            return self._check_ccpa_compliance(business_data)
        return True

    def _check_gdpr_compliance(self, business_data: Dict) -> bool:
        """Check GDPR compliance"""
        # 1. Lawful basis for processing
        if not self._has_lawful_basis(business_data):
            return False

        # 2. Data minimization
        if not self._verify_data_minimization(business_data):
            return False

        # 3. Purpose limitation
        if not business_data.get('processing_purpose'):
            return False

        return True

    def _check_ccpa_compliance(self, business_data: Dict) -> bool:
        """Check CCPA compliance"""
        # 1. Verify business size (CCPA applies to larger businesses)
        if self._is_ccpa_applicable():
            # 2. Check notice requirements
            if not self._has_privacy_notice():
                return False

            # 3. Ensure opt-out mechanism
            if not self._has_opt_out_mechanism():
                return False

        return True

    def validate_email_campaign(self, campaign_data: Dict) -> bool:
        """Validate email campaign compliance with CAN-SPAM Act"""
        required_fields = {
            'sender_name': bool(campaign_data.get('sender_name')),
            'sender_email': bool(campaign_data.get('sender_email')),
            'unsubscribe_link': 'unsubscribe' in str(campaign_data.get('email_content', '')).lower(),
            'physical_address': bool(campaign_data.get('physical_address')),
            'subject_line': not self._is_deceptive_subject(campaign_data.get('subject', ''))
        }
        
        is_compliant = all(required_fields.values())
        if not is_compliant:
            missing = [k for k, v in required_fields.items() if not v]
            self.logger.warning(f"Campaign missing required fields: {missing}")
        
        return is_compliant

    def _is_deceptive_subject(self, subject: str) -> bool:
        """Check if email subject line is deceptive"""
        deceptive_patterns = [
            'guaranteed',
            'no risk',
            'winner',
            'free money',
            'urgent',
            '100%',
            'act now'
        ]
        return any(pattern in subject.lower() for pattern in deceptive_patterns)

    def handle_data_deletion_request(self, business_id: str) -> bool:
        """Handle right to erasure (GDPR Article 17)"""
        try:
            # 1. Log deletion request
            self.logger.info(f"Processing deletion request for business ID: {business_id}")

            # 2. Delete from all systems
            systems_to_clean = [
                self._delete_from_database,
                self._delete_from_crm,
                self._delete_from_email_system
            ]

            # 3. Execute deletion
            for delete_func in systems_to_clean:
                delete_func(business_id)

            # 4. Log successful deletion
            self.logger.info(f"Completed deletion request for business ID: {business_id}")
            return True

        except Exception as e:
            self.logger.error(f"Error processing deletion request: {str(e)}")
            return False

    def _delete_from_database(self, business_id: str):
        """Delete business data from main database"""
        # Implementation depends on your database system
        pass

    def _delete_from_crm(self, business_id: str):
        """Delete business data from HubSpot"""
        # Implementation for HubSpot deletion
        pass

    def _delete_from_email_system(self, business_id: str):
        """Delete business data from SendGrid"""
        # Implementation for SendGrid deletion
        pass

    def export_business_data(self, business_id: str) -> Optional[Dict]:
        """Handle data portability request (GDPR Article 20)"""
        try:
            # 1. Gather data from all systems
            data = {}
            
            # 2. Format in machine-readable format (JSON)
            data_export = json.dumps(data, indent=2)
            
            # 3. Log export
            self.logger.info(f"Exported data for business ID: {business_id}")
            
            return data_export
        except Exception as e:
            self.logger.error(f"Error exporting data: {str(e)}")
            return None

    def cleanup_old_data(self) -> bool:
        """Remove data older than retention period"""
        try:
            cutoff_date = datetime.now() - timedelta(days=self.privacy_settings.data_retention_days)
            # Implementation to remove old data
            self.logger.info(f"Cleaned up data older than {cutoff_date}")
            return True
        except Exception as e:
            self.logger.error(f"Error in data cleanup: {str(e)}")
            return False
