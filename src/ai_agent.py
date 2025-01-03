import json
import os
import openai
from datetime import datetime
from dotenv import load_dotenv
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

load_dotenv()

class AIAgent:
    def __init__(self):
        self.openai_key = os.getenv('OPENAI_API_KEY')
        openai.api_key = self.openai_key
        self.response_history_file = 'data/response_history.json'
        self.business_insights_file = 'data/business_insights.json'
        self.load_history()
        self.load_insights()

        # Business type patterns and indicators
        self.business_patterns = {
            'restaurant': {
                'keywords': ['restaurant', 'cafe', 'diner', 'bistro', 'eatery', 'food'],
                'pain_points': ['online ordering', 'reservation system', 'menu updates', 'food photos'],
                'opportunities': ['food delivery', 'online menu', 'table reservations', 'customer reviews'],
                'success_metrics': ['order volume', 'reservation rate', 'customer reviews', 'menu views']
            },
            'retail': {
                'keywords': ['retail', 'store', 'shop', 'boutique', 'market'],
                'pain_points': ['inventory management', 'online sales', 'product showcase', 'payment processing'],
                'opportunities': ['e-commerce', 'inventory system', 'product catalog', 'online payments'],
                'success_metrics': ['online sales', 'inventory turnover', 'cart completion', 'product views']
            },
            'salon': {
                'keywords': ['salon', 'spa', 'beauty', 'hair', 'nails', 'barber'],
                'pain_points': ['appointment scheduling', 'service showcase', 'staff scheduling', 'customer retention'],
                'opportunities': ['online booking', 'service catalog', 'staff profiles', 'loyalty program'],
                'success_metrics': ['booking rate', 'repeat customers', 'service popularity', 'customer feedback']
            },
            'gym': {
                'keywords': ['gym', 'fitness', 'workout', 'training', 'yoga', 'crossfit'],
                'pain_points': ['class scheduling', 'membership management', 'trainer booking', 'attendance tracking'],
                'opportunities': ['class registration', 'membership portal', 'trainer profiles', 'workout tracking'],
                'success_metrics': ['membership growth', 'class attendance', 'trainer bookings', 'member retention']
            },
            'automotive': {
                'keywords': ['auto', 'car', 'mechanic', 'repair', 'service', 'tire'],
                'pain_points': ['service scheduling', 'repair tracking', 'parts inventory', 'customer communication'],
                'opportunities': ['online appointments', 'service history', 'status updates', 'maintenance reminders'],
                'success_metrics': ['service bookings', 'customer retention', 'parts sales', 'review ratings']
            },
            'professional': {
                'keywords': ['lawyer', 'accountant', 'consultant', 'insurance', 'real estate', 'professional'],
                'pain_points': ['client scheduling', 'document sharing', 'client communication', 'service explanation'],
                'opportunities': ['online consultations', 'document portal', 'service packages', 'testimonials'],
                'success_metrics': ['consultation rate', 'client retention', 'document usage', 'referral rate']
            }
        }

    def load_history(self):
        """Load response history from file"""
        try:
            with open(self.response_history_file, 'r') as f:
                self.response_history = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.response_history = []

    def load_insights(self):
        """Load business insights from file"""
        try:
            with open(self.business_insights_file, 'r') as f:
                self.business_insights = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.business_insights = {}

    def save_history(self):
        """Save response history to file"""
        os.makedirs(os.path.dirname(self.response_history_file), exist_ok=True)
        with open(self.response_history_file, 'w') as f:
            json.dump(self.response_history, f, indent=2)

    def save_insights(self):
        """Save business insights to file"""
        os.makedirs(os.path.dirname(self.business_insights_file), exist_ok=True)
        with open(self.business_insights_file, 'w') as f:
            json.dump(self.business_insights, f, indent=2)

    def analyze_business(self, business_data):
        """
        Analyze business data to determine type, opportunities, and personalization
        Returns dict with business analysis
        """
        # Extract business information
        business_info = ' '.join([
            business_data.get('name', '').lower(),
            business_data.get('description', ''),
            business_data.get('categories', '')
        ])

        # Detect business type
        business_type, confidence = self._detect_business_type(business_info)
        
        # Get business patterns
        patterns = self.business_patterns.get(business_type, self.business_patterns['professional'])
        
        # Generate personalized insights using GPT
        prompt = f"""
        Analyze this business for website opportunities:
        Business Name: {business_data.get('name')}
        Business Type: {business_type}
        Description: {business_data.get('description')}
        Known Pain Points: {', '.join(patterns['pain_points'])}
        Opportunities: {', '.join(patterns['opportunities'])}
        
        Provide specific recommendations for their website.
        """
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "system", "content": "You are a web development expert specializing in business websites."},
                         {"role": "user", "content": prompt}]
            )
            insights = response.choices[0].message.content
        except Exception as e:
            print(f"Error getting GPT insights: {e}")
            insights = "Unable to generate insights at this time."

        return {
            'business_type': business_type,
            'confidence': confidence,
            'patterns': patterns,
            'insights': insights,
            'analysis_date': datetime.now().isoformat()
        }

    def _detect_business_type(self, business_info):
        """
        Detect business type using TF-IDF and cosine similarity
        Returns tuple of (type, confidence)
        """
        # Create TF-IDF vectors for business patterns
        pattern_texts = []
        pattern_types = []
        
        for btype, pattern in self.business_patterns.items():
            pattern_text = ' '.join(pattern['keywords'])
            pattern_texts.append(pattern_text)
            pattern_types.append(btype)

        # Add the business info
        all_texts = pattern_texts + [business_info]
        
        # Create TF-IDF matrix
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(all_texts)
        
        # Calculate similarity between business and each pattern
        business_vector = tfidf_matrix[-1]
        pattern_vectors = tfidf_matrix[:-1]
        
        similarities = cosine_similarity(business_vector, pattern_vectors)[0]
        
        # Get best match
        best_match_idx = np.argmax(similarities)
        confidence = similarities[best_match_idx]
        
        return pattern_types[best_match_idx], float(confidence)

    def generate_email(self, business_analysis, template_type='custom'):
        """
        Generate personalized email using business analysis and GPT
        Returns dict with email subject and content
        """
        patterns = business_analysis['patterns']
        insights = business_analysis['insights']
        
        prompt = f"""
        Create a personalized email for this business:
        Business Analysis: {insights}
        Pain Points: {', '.join(patterns['pain_points'])}
        Opportunities: {', '.join(patterns['opportunities'])}
        
        The email should:
        1. Address their specific pain points
        2. Highlight relevant opportunities
        3. Offer concrete solutions
        4. Include a clear call to action
        
        Use a professional but conversational tone.
        """
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "system", "content": "You are a professional web developer reaching out to businesses."},
                         {"role": "user", "content": prompt}]
            )
            
            email_content = response.choices[0].message.content
            
            # Save to response history
            self.response_history.append({
                'date': datetime.now().isoformat(),
                'business_type': business_analysis['business_type'],
                'template_type': template_type,
                'content': email_content
            })
            self.save_history()
            
            return {
                'subject': f"Website Opportunity for {business_analysis.get('business_name', 'Your Business')}",
                'content': email_content
            }
            
        except Exception as e:
            print(f"Error generating email: {e}")
            return None

    def learn_from_response(self, email_id, response_type, response_data):
        """
        Learn from email responses to improve future communications
        """
        if email_id in self.response_history:
            email_record = self.response_history[email_id]
            business_type = email_record['business_type']
            
            # Update business insights
            if business_type not in self.business_insights:
                self.business_insights[business_type] = {
                    'responses': {'positive': 0, 'negative': 0, 'neutral': 0},
                    'effective_phrases': [],
                    'ineffective_phrases': []
                }
            
            insights = self.business_insights[business_type]
            insights['responses'][response_type] += 1
            
            # Analyze response content for effective/ineffective phrases
            if response_data.get('content'):
                prompt = f"""
                Analyze this email response for key phrases that made it {response_type}:
                {response_data['content']}
                
                Extract:
                1. Effective phrases that resonated
                2. Ineffective phrases to avoid
                """
                
                try:
                    response = openai.ChatCompletion.create(
                        model="gpt-4",
                        messages=[{"role": "system", "content": "You are analyzing email responses for effectiveness."},
                                 {"role": "user", "content": prompt}]
                    )
                    
                    analysis = response.choices[0].message.content
                    
                    # Update insights
                    if response_type == 'positive':
                        insights['effective_phrases'].extend(analysis.get('effective', []))
                    else:
                        insights['ineffective_phrases'].extend(analysis.get('ineffective', []))
                    
                    self.save_insights()
                    
                except Exception as e:
                    print(f"Error analyzing response: {e}")

    def get_performance_metrics(self):
        """
        Get performance metrics for email campaigns
        """
        metrics = {
            'total_emails': len(self.response_history),
            'response_rates': {},
            'business_type_performance': {}
        }
        
        for business_type in self.business_patterns.keys():
            if business_type in self.business_insights:
                insights = self.business_insights[business_type]
                responses = insights['responses']
                total = sum(responses.values())
                
                if total > 0:
                    metrics['business_type_performance'][business_type] = {
                        'total_emails': total,
                        'positive_rate': responses['positive'] / total,
                        'response_rate': (responses['positive'] + responses['negative']) / total,
                        'top_phrases': insights['effective_phrases'][:5]
                    }
        
        return metrics
