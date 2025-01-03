import json
import os
import openai
from datetime import datetime
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from textblob import TextBlob
import requests
from bs4 import BeautifulSoup
import yfinance as yf
from dotenv import load_dotenv

load_dotenv()

class EnhancedAIAgent:
    def __init__(self):
        self.openai_key = os.getenv('OPENAI_API_KEY')
        openai.api_key = self.openai_key
        self.data_dir = 'data'
        self.setup_data_directory()
        self.load_data()
        
        # Initialize learning parameters
        self.learning_rate = 0.1
        self.exploration_rate = 0.2
        self.min_confidence_threshold = 0.7

    def setup_data_directory(self):
        """Setup data directory and files"""
        os.makedirs(self.data_dir, exist_ok=True)
        self.files = {
            'response_history': os.path.join(self.data_dir, 'response_history.json'),
            'business_insights': os.path.join(self.data_dir, 'business_insights.json'),
            'market_trends': os.path.join(self.data_dir, 'market_trends.json'),
            'competitor_data': os.path.join(self.data_dir, 'competitor_data.json'),
            'ab_tests': os.path.join(self.data_dir, 'ab_tests.json'),
            'reinforcement_data': os.path.join(self.data_dir, 'reinforcement_data.json')
        }

    def load_data(self):
        """Load all data files"""
        self.data = {}
        for key, filepath in self.files.items():
            try:
                with open(filepath, 'r') as f:
                    self.data[key] = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                self.data[key] = {}
        
        # Initialize if empty
        if not self.data['reinforcement_data']:
            self.data['reinforcement_data'] = {
                'state_values': {},
                'action_values': {},
                'rewards': []
            }

    def save_data(self):
        """Save all data files"""
        for key, filepath in self.files.items():
            with open(filepath, 'w') as f:
                json.dump(self.data[key], f, indent=2)

    def analyze_market_trends(self, business_type):
        """Analyze market trends for business type"""
        try:
            # Get industry keywords
            keywords = self._get_industry_keywords(business_type)
            
            # Search news and analyze sentiment
            news_sentiment = self._analyze_news_sentiment(keywords)
            
            # Get market data if available
            market_data = self._get_market_data(business_type)
            
            # Combine insights
            trends = {
                'sentiment': news_sentiment,
                'market_data': market_data,
                'timestamp': datetime.now().isoformat()
            }
            
            # Save trends
            self.data['market_trends'][business_type] = trends
            self.save_data()
            
            return trends
            
        except Exception as e:
            print(f"Error analyzing market trends: {e}")
            return None

    def _analyze_news_sentiment(self, keywords):
        """Analyze news sentiment for keywords"""
        news_urls = self._search_news(keywords)
        sentiments = []
        
        for url in news_urls[:5]:  # Analyze top 5 news articles
            try:
                text = self._scrape_text(url)
                blob = TextBlob(text)
                sentiments.append(blob.sentiment.polarity)
            except:
                continue
        
        return np.mean(sentiments) if sentiments else 0

    def _get_market_data(self, business_type):
        """Get relevant market data"""
        # Map business types to stock symbols
        industry_etfs = {
            'restaurant': 'EATZ',
            'retail': 'XRT',
            'technology': 'VGT',
            'healthcare': 'VHT'
        }
        
        if business_type in industry_etfs:
            try:
                ticker = yf.Ticker(industry_etfs[business_type])
                data = ticker.history(period='1mo')
                return {
                    'current_price': float(data['Close'][-1]),
                    'monthly_change': float(data['Close'][-1] - data['Close'][0]) / data['Close'][0]
                }
            except:
                return None
        return None

    def analyze_competitors(self, business_data):
        """Analyze competitors in the area"""
        try:
            location = business_data.get('location', '')
            business_type = business_data.get('type', '')
            
            # Search for competitors
            competitors = self._search_competitors(location, business_type)
            
            # Analyze competitor websites
            competitor_analysis = []
            for competitor in competitors:
                if competitor.get('website'):
                    analysis = self._analyze_website(competitor['website'])
                    competitor_analysis.append({
                        'name': competitor['name'],
                        'website': competitor['website'],
                        'features': analysis['features'],
                        'strengths': analysis['strengths'],
                        'weaknesses': analysis['weaknesses']
                    })
            
            return competitor_analysis
            
        except Exception as e:
            print(f"Error analyzing competitors: {e}")
            return []

    def _analyze_website(self, url):
        """Analyze website features and content"""
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Analyze features
            features = {
                'has_booking': bool(soup.find_all(string=re.compile('book|schedule|appointment', re.I))),
                'has_contact': bool(soup.find_all(string=re.compile('contact|email|phone', re.I))),
                'has_products': bool(soup.find_all(string=re.compile('product|shop|store', re.I))),
                'has_social': bool(soup.find_all(href=re.compile('facebook|twitter|instagram', re.I)))
            }
            
            return {
                'features': features,
                'strengths': self._analyze_strengths(soup),
                'weaknesses': self._analyze_weaknesses(soup)
            }
            
        except Exception as e:
            print(f"Error analyzing website: {e}")
            return {'features': {}, 'strengths': [], 'weaknesses': []}

    def run_ab_test(self, test_name, variants):
        """Run A/B test on email variants"""
        if test_name not in self.data['ab_tests']:
            self.data['ab_tests'][test_name] = {
                'variants': variants,
                'results': {variant['id']: {'sends': 0, 'responses': 0} for variant in variants},
                'start_date': datetime.now().isoformat()
            }
        
        # Select variant using epsilon-greedy strategy
        if random.random() < self.exploration_rate:
            # Explore: random selection
            selected_variant = random.choice(variants)
        else:
            # Exploit: select best performing
            results = self.data['ab_tests'][test_name]['results']
            response_rates = {
                variant_id: results[variant_id]['responses'] / max(results[variant_id]['sends'], 1)
                for variant_id in results
            }
            selected_variant = max(response_rates.items(), key=lambda x: x[1])[0]
        
        return selected_variant

    def update_ab_test(self, test_name, variant_id, response):
        """Update A/B test results"""
        if test_name in self.data['ab_tests']:
            results = self.data['ab_tests'][test_name]['results']
            if variant_id in results:
                results[variant_id]['sends'] += 1
                if response:
                    results[variant_id]['responses'] += 1
            self.save_data()

    def get_personalized_content(self, business_data, content_type='email'):
        """Generate highly personalized content"""
        try:
            # Gather all context
            market_trends = self.analyze_market_trends(business_data['type'])
            competitor_analysis = self.analyze_competitors(business_data)
            business_insights = self.data['business_insights'].get(business_data['type'], {})
            
            # Create rich context for GPT
            context = {
                'business': business_data,
                'market_trends': market_trends,
                'competitors': competitor_analysis,
                'insights': business_insights,
                'successful_phrases': self._get_successful_phrases(business_data['type'])
            }
            
            # Generate content using GPT
            prompt = self._create_rich_prompt(context, content_type)
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert in business communication and web development."},
                    {"role": "user", "content": prompt}
                ]
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error generating personalized content: {e}")
            return None

    def _create_rich_prompt(self, context, content_type):
        """Create detailed prompt with all context"""
        return f"""
        Create {content_type} content for this business:
        
        Business Information:
        - Name: {context['business'].get('name')}
        - Type: {context['business'].get('type')}
        - Location: {context['business'].get('location')}
        
        Market Context:
        - Market Sentiment: {context['market_trends'].get('sentiment')}
        - Industry Trends: {context['market_trends'].get('market_data')}
        
        Competitor Analysis:
        {self._format_competitor_analysis(context['competitors'])}
        
        Previous Success Patterns:
        - Effective Phrases: {', '.join(context['successful_phrases'])}
        
        The content should:
        1. Address current market conditions
        2. Differentiate from competitors
        3. Use proven successful phrases
        4. Include specific, actionable value propositions
        5. Maintain a professional but engaging tone
        """

    def _format_competitor_analysis(self, competitors):
        """Format competitor analysis for prompt"""
        if not competitors:
            return "No competitor data available"
            
        analysis = []
        for comp in competitors:
            analysis.append(f"""
            Competitor: {comp['name']}
            - Key Features: {', '.join(comp['features'])}
            - Strengths: {', '.join(comp['strengths'])}
            - Weaknesses: {', '.join(comp['weaknesses'])}
            """)
        return '\n'.join(analysis)

    def chat_response(self, message, context=None):
        """Generate chat response"""
        try:
            # Analyze intent
            intent = self._analyze_intent(message)
            
            # Get relevant context
            if context is None:
                context = self._get_relevant_context(intent)
            
            # Generate response using GPT
            prompt = f"""
            User Message: {message}
            Intent: {intent}
            Context: {json.dumps(context)}
            
            Respond as a helpful AI assistant specializing in business websites and marketing.
            Be concrete and specific in your advice and suggestions.
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant specializing in business websites and marketing."},
                    {"role": "user", "content": prompt}
                ]
            )
            
            return {
                'response': response.choices[0].message.content,
                'intent': intent,
                'context': context
            }
            
        except Exception as e:
            print(f"Error generating chat response: {e}")
            return {
                'response': "I apologize, but I'm having trouble processing your request. Could you please try again?",
                'intent': 'error',
                'context': {}
            }

    def _analyze_intent(self, message):
        """Analyze user message intent"""
        intents = {
            'analyze': ['analyze', 'review', 'check', 'look at'],
            'template': ['template', 'email', 'message', 'write'],
            'insights': ['insights', 'trends', 'data', 'performance'],
            'help': ['help', 'how to', 'what is', 'explain']
        }
        
        message = message.lower()
        for intent, keywords in intents.items():
            if any(keyword in message for keyword in keywords):
                return intent
        return 'general'

    def _get_relevant_context(self, intent):
        """Get relevant context based on intent"""
        context = {}
        
        if intent == 'analyze':
            context['market_trends'] = self.data['market_trends']
        elif intent == 'template':
            context['successful_templates'] = self._get_successful_templates()
        elif intent == 'insights':
            context['performance_metrics'] = self.get_performance_metrics()
        
        return context

    def update_learning(self, state, action, reward):
        """Update reinforcement learning data"""
        state_key = json.dumps(state)
        action_key = json.dumps(action)
        
        # Update state-action values
        if state_key not in self.data['reinforcement_data']['state_values']:
            self.data['reinforcement_data']['state_values'][state_key] = 0
        
        if action_key not in self.data['reinforcement_data']['action_values']:
            self.data['reinforcement_data']['action_values'][action_key] = 0
        
        # Update values using Q-learning
        current_value = self.data['reinforcement_data']['action_values'][action_key]
        new_value = current_value + self.learning_rate * (reward - current_value)
        self.data['reinforcement_data']['action_values'][action_key] = new_value
        
        # Store reward
        self.data['reinforcement_data']['rewards'].append({
            'state': state,
            'action': action,
            'reward': reward,
            'timestamp': datetime.now().isoformat()
        })
        
        self.save_data()

    def get_best_action(self, state):
        """Get best action for given state based on learned values"""
        state_key = json.dumps(state)
        action_values = self.data['reinforcement_data']['action_values']
        
        # Use epsilon-greedy strategy
        if random.random() < self.exploration_rate:
            # Explore: random action
            return random.choice(list(action_values.keys()))
        else:
            # Exploit: best known action
            if action_values:
                return max(action_values.items(), key=lambda x: x[1])[0]
            return None

    def get_performance_metrics(self):
        """Get comprehensive performance metrics"""
        metrics = {
            'response_rates': self._calculate_response_rates(),
            'ab_test_results': self._get_ab_test_results(),
            'learning_progress': self._get_learning_progress(),
            'market_impact': self._analyze_market_impact()
        }
        return metrics

    def _calculate_response_rates(self):
        """Calculate detailed response rates"""
        rates = {}
        for business_type in self.data['business_insights']:
            responses = self.data['business_insights'][business_type]['responses']
            total = sum(responses.values())
            if total > 0:
                rates[business_type] = {
                    'positive_rate': responses['positive'] / total,
                    'response_rate': (responses['positive'] + responses['negative']) / total,
                    'total_emails': total
                }
        return rates

    def _get_ab_test_results(self):
        """Get results of all A/B tests"""
        results = {}
        for test_name, test_data in self.data['ab_tests'].items():
            variants = test_data['results']
            results[test_name] = {
                variant_id: {
                    'response_rate': variants[variant_id]['responses'] / max(variants[variant_id]['sends'], 1),
                    'total_sends': variants[variant_id]['sends']
                }
                for variant_id in variants
            }
        return results

    def _get_learning_progress(self):
        """Analyze learning progress"""
        rewards = self.data['reinforcement_data']['rewards']
        if rewards:
            recent_rewards = rewards[-100:]  # Look at last 100 rewards
            return {
                'average_reward': np.mean([r['reward'] for r in recent_rewards]),
                'reward_trend': np.polyfit([i for i in range(len(recent_rewards))],
                                         [r['reward'] for r in recent_rewards],
                                         1)[0]
            }
        return {'average_reward': 0, 'reward_trend': 0}
