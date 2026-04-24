"""
Advanced AI Chatbot for Farmers
Provides intelligent responses to farming queries
"""

import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class FarmingChatbot:
    def __init__(self):
        self.knowledge_base = self._build_knowledge_base()
    
    def _build_knowledge_base(self):
        """Comprehensive farming knowledge base"""
        return {
            # Crop Selection
            'crop_selection': {
                'keywords': ['which crop', 'what crop', 'best crop', 'grow crop', 'plant crop', 'crop recommendation'],
                'responses': {
                    'kharif': 'For Kharif season (June-October), grow: Rice, Cotton, Maize, Soybean, Groundnut, Sugarcane. These crops need monsoon rainfall.',
                    'rabi': 'For Rabi season (October-March), grow: Wheat, Barley, Mustard, Chickpea, Lentil, Peas. These crops need cool weather.',
                    'zaid': 'For Zaid season (March-June), grow: Watermelon, Cucumber, Muskmelon, Vegetables. These are summer crops.',
                    'july': 'In July, plant Kharif crops: Rice, Cotton, Maize, Soybean. Monsoon is perfect for these.',
                    'january': 'In January, Rabi crops are growing. Focus on irrigation and fertilizer for Wheat, Chickpea.',
                    'default': 'Check our AI Crop Recommendation on dashboard. It analyzes your soil, weather, and suggests best crops with profit estimates.'
                }
            },
            
            # Weather & Climate
            'weather': {
                'keywords': ['weather', 'rain', 'temperature', 'climate', 'forecast', 'monsoon'],
                'response': 'Check Weather section for 7-day forecast with temperature, humidity, and rainfall. We provide real-time data from OpenWeatherMap API. Plan irrigation and harvesting based on weather predictions.'
            },
            
            # Irrigation
            'irrigation': {
                'keywords': ['irrigation', 'water', 'watering', 'drip', 'sprinkler'],
                'response': 'Best irrigation practices:\n• Use drip irrigation - saves 30-40% water\n• Water early morning (6-8 AM) or evening (5-7 PM)\n• Check soil moisture before watering\n• For drip: 2-3 hours daily\n• For sprinkler: 1-2 hours every 2-3 days\n• Avoid over-watering - causes root rot'
            },
            
            # Fertilizers
            'fertilizer': {
                'keywords': ['fertilizer', 'npk', 'urea', 'dap', 'manure', 'compost', 'nutrients'],
                'response': 'Fertilizer guide:\n• Nitrogen (N) - Urea: 40-50 kg/hectare for leafy growth\n• Phosphorus (P) - DAP: 50-60 kg/hectare for roots and flowers\n• Potassium (K) - MOP: 30-40 kg/hectare for fruit quality\n• Organic: Compost 5-10 tons/hectare\n• Apply in 3 splits: Base, 30 days, 60 days after sowing\n• Get soil test every 6 months'
            },
            
            # Pest & Disease
            'pest_disease': {
                'keywords': ['pest', 'disease', 'insect', 'fungus', 'aphid', 'blight', 'wilt', 'leaf'],
                'response': 'Pest & Disease management:\n• Upload crop image for AI disease detection\n• Organic: Neem oil spray (5ml/liter water)\n• Chemical: Use only when necessary\n• Preventive: Crop rotation, clean field\n• Common pests: Aphids, Whitefly, Bollworm\n• Common diseases: Leaf Blight, Powdery Mildew, Wilt\n• Spray early morning or evening'
            },
            
            # Soil Health
            'soil': {
                'keywords': ['soil', 'ph', 'nitrogen', 'phosphorus', 'potassium', 'soil test'],
                'response': 'Soil health tips:\n• Ideal pH: 6.0-7.5 for most crops\n• Get soil test every 6 months (₹50-100)\n• If acidic (pH<6): Add lime 200-500 kg/hectare\n• If alkaline (pH>8): Add gypsum 500-1000 kg/hectare\n• Add organic matter: Compost, FYM, green manure\n• Avoid burning crop residue - make compost instead\n• Practice crop rotation'
            },
            
            # Market Prices
            'market': {
                'keywords': ['price', 'market', 'mandi', 'sell', 'rate', 'cost'],
                'response': 'Market prices updated daily from government Mandi API. Check Market section for:\n• Current prices of all crops\n• Price trends (up/down/stable)\n• Best time to sell\n• Compare prices across crops\n• We show REAL prices from data.gov.in'
            },
            
            # Profit & Finance
            'profit': {
                'keywords': ['profit', 'income', 'revenue', 'cost', 'expense', 'roi', 'money'],
                'response': 'Maximize profit:\n• Use our Profit Calculator on dashboard\n• Formula: Profit = (Yield × Price) - Costs\n• Reduce costs: Use drip irrigation, organic fertilizer\n• Increase yield: Proper fertilizer, pest control\n• Sell at right time: Check market trends\n• Track expenses in Finance section\n• Average ROI: 40-60% for good farming'
            },
            
            # Government Schemes
            'schemes': {
                'keywords': ['scheme', 'subsidy', 'pm-kisan', 'loan', 'insurance', 'government'],
                'response': 'Government schemes for farmers:\n• PM-KISAN: ₹6000/year direct transfer (all farmers)\n• Kisan Credit Card: Low interest loans (7% interest)\n• PM Fasal Bima: Crop insurance at 2% premium\n• Soil Health Card: Free soil testing\n• Drip irrigation subsidy: 50-90% subsidy\n• Apply online at pmkisan.gov.in'
            },
            
            # Organic Farming
            'organic': {
                'keywords': ['organic', 'natural', 'chemical-free', 'bio', 'vermicompost'],
                'response': 'Organic farming tips:\n• Use vermicompost: 2-3 tons/hectare\n• Neem oil for pests: 5ml/liter water\n• Cow urine spray: 10% solution\n• Green manure: Grow Dhaincha, Sunhemp\n• Crop rotation: Legumes → Cereals\n• Mulching: Saves water, controls weeds\n• Certification: Apply for organic certificate after 3 years'
            },
            
            # Harvesting
            'harvest': {
                'keywords': ['harvest', 'harvesting', 'reap', 'cutting', 'maturity'],
                'response': 'Harvesting guide:\n• Rice: 30-35 days after flowering (golden yellow)\n• Wheat: 110-120 days after sowing (grain hard)\n• Cotton: 150-180 days (bolls open, fluffy)\n• Harvest early morning for better quality\n• Dry grains to 12-14% moisture before storage\n• Use combine harvester to save labor\n• Rent equipment from our Equipment section'
            },
            
            # Storage
            'storage': {
                'keywords': ['storage', 'store', 'godown', 'warehouse', 'preserve'],
                'response': 'Proper storage methods:\n• Dry grains to 12-14% moisture\n• Use airtight containers or hermetic bags\n• Store in cool, dry place away from sunlight\n• Check regularly for pests and moisture\n• Use neem leaves as natural pest repellent\n• For long-term: Use fumigation\n• Government warehouses available at low cost'
            },
            
            # Labor Management
            'labor': {
                'keywords': ['labor', 'worker', 'wage', 'manpower', 'hiring'],
                'response': 'Labor management:\n• Current wage: ₹400-600/day (varies by region)\n• Peak season: Sowing and harvesting need more labor\n• Use our Labor Management section to track workers\n• Consider mechanization to reduce labor dependency\n• Provide drinking water and shade for workers\n• Pay on time to maintain good relations'
            },
            
            # Equipment
            'equipment': {
                'keywords': ['tractor', 'equipment', 'machinery', 'tools', 'harvester', 'rent'],
                'response': 'Farm equipment:\n• Tractor rent: ₹800-1200/day\n• Harvester rent: ₹1500-2000/day\n• Sprayer rent: ₹300-500/day\n• Check our Equipment Rental section\n• Government subsidy: 40-50% on equipment\n• Custom Hiring Centers: Rent at low cost\n• Maintain equipment regularly'
            }
        }
    
    def get_response(self, user_message):
        """Get intelligent response based on user query"""
        try:
            message = user_message.lower().strip()
            
            # Check for greetings
            if any(word in message for word in ['hello', 'hi', 'hey', 'namaste']):
                return "🙏 Namaste! I'm your AI Farming Assistant. Ask me about crops, weather, irrigation, fertilizers, pests, market prices, or any farming question!"
            
            # Check for thanks
            if any(word in message for word in ['thank', 'thanks', 'धन्यवाद']):
                return "You're welcome! Happy farming! 🌾 Feel free to ask more questions anytime."
            
            # Month-specific crop queries
            months = {
                'january': 'january', 'jan': 'january',
                'february': 'rabi', 'feb': 'rabi',
                'march': 'zaid', 'mar': 'zaid',
                'april': 'zaid', 'apr': 'zaid',
                'may': 'zaid',
                'june': 'kharif', 'jun': 'kharif',
                'july': 'july', 'jul': 'july',
                'august': 'kharif', 'aug': 'kharif',
                'september': 'kharif', 'sep': 'kharif',
                'october': 'rabi', 'oct': 'rabi',
                'november': 'rabi', 'nov': 'rabi',
                'december': 'rabi', 'dec': 'rabi'
            }
            
            for month_key, season in months.items():
                if month_key in message:
                    if 'crop_selection' in self.knowledge_base:
                        responses = self.knowledge_base['crop_selection']['responses']
                        return responses.get(season, responses['default'])
            
            # Check each knowledge category
            for category, data in self.knowledge_base.items():
                keywords = data.get('keywords', [])
                
                # Check if any keyword matches
                if any(keyword in message for keyword in keywords):
                    if 'responses' in data:
                        # Handle multiple responses
                        for key, response in data['responses'].items():
                            if key in message or key == 'default':
                                return response
                    else:
                        return data.get('response', '')
            
            # Default response with suggestions
            return """I can help you with:
            
🌾 **Crops**: Which crop to grow, seasonal crops
🌦️ **Weather**: Forecast, rainfall, temperature
💧 **Irrigation**: Drip, sprinkler, water management
🧪 **Fertilizers**: NPK, organic, application timing
🐛 **Pests & Diseases**: Identification, treatment
🌱 **Soil**: pH, nutrients, soil testing
💰 **Market Prices**: Current rates, trends
📊 **Profit**: Calculate income, reduce costs
🏛️ **Government Schemes**: PM-KISAN, loans, insurance
🌿 **Organic Farming**: Natural methods
🚜 **Equipment**: Tractor, harvester rental
👷 **Labor**: Wage rates, management

Ask me anything! Example: "What crop should I grow in July?" or "How to control pests?"
"""
        
        except Exception as e:
            logger.error(f"Chatbot error: {e}")
            return "Sorry, I couldn't understand that. Please try asking in a different way or check the dashboard for detailed information."

# Global chatbot instance
farming_chatbot = FarmingChatbot()

def get_chatbot_response(message):
    """Get response from farming chatbot"""
    return farming_chatbot.get_response(message)
