# AI Chatbot Service using OpenAI GPT

import openai

class ChatbotService:
    def __init__(self, api_key):
        openai.api_key = api_key
        self.system_prompt = """You are an expert agricultural advisor helping farmers in India. 
        Provide practical, actionable advice about:
        - Crop selection and farming techniques
        - Soil health and fertilizers
        - Pest control and disease management
        - Weather-based recommendations
        - Market prices and selling strategies
        - Government schemes for farmers
        
        Keep responses concise (2-3 sentences), practical, and in simple language.
        Use Indian context (₹ for currency, local crop names, Indian seasons)."""
    
    def get_response(self, user_message, context=None):
        """
        Get AI response for user question
        
        Args:
            user_message: User's question
            context: Optional context (soil data, weather, etc.)
            
        Returns:
            str: AI response
        """
        try:
            messages = [
                {"role": "system", "content": self.system_prompt}
            ]
            
            # Add context if provided
            if context:
                context_msg = f"User's farm context: {context}"
                messages.append({"role": "system", "content": context_msg})
            
            messages.append({"role": "user", "content": user_message})
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=150,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Chatbot error: {e}")
            return self._fallback_response(user_message)
    
    def _fallback_response(self, question):
        """Fallback responses when API fails"""
        question_lower = question.lower()
        
        responses = {
            'weather': 'Check the weather section for current conditions and 7-day forecast. Plan your farming activities accordingly.',
            'pest': 'For pest control, use neem oil spray as an organic solution. For severe cases, consult the disease detection feature.',
            'fertilizer': 'Apply NPK fertilizer based on your soil test results. Check the soil analysis section for specific recommendations.',
            'irrigation': 'Water crops early morning or evening. Use drip irrigation to save 30% water. Check soil moisture regularly.',
            'crop': 'Use our AI crop recommendation feature for personalized suggestions based on your soil and weather conditions.',
            'price': 'Check the market prices section for current rates. Sell when prices are trending upward.',
            'loan': 'Check the loan & insurance section for eligibility and application process.',
            'scheme': 'Popular schemes: PM-KISAN (₹6000/year), Fasal Bima Yojana (crop insurance), Kisan Credit Card (low interest loans).'
        }
        
        for key, response in responses.items():
            if key in question_lower:
                return response
        
        return "I can help with weather, pests, fertilizers, irrigation, crops, market prices, loans, and government schemes. What would you like to know?"


# Usage in app.py:
"""
from chatbot_service import ChatbotService

# Initialize chatbot
chatbot = ChatbotService(api_key="YOUR_OPENAI_API_KEY")

@app.route('/api/chatbot', methods=['POST'])
def chatbot_endpoint():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    question = data.get('question', '')
    
    # Get user context
    user = User.query.get(session['user_id'])
    soil_data = get_user_soil_data(user.id)
    weather, _ = get_weather_data(user.location)
    
    # Build context
    context = f"Location: {user.location}, Farm size: {user.farm_size} hectares, "
    context += f"Soil pH: {soil_data['ph']}, Temperature: {weather['temperature']}°C"
    
    # Get AI response
    response = chatbot.get_response(question, context)
    
    return jsonify({'response': response})

# Advanced: Conversation history
@app.route('/api/chatbot/conversation', methods=['POST'])
def chatbot_conversation():
    data = request.get_json()
    messages = data.get('messages', [])  # Array of {role, content}
    
    # Add system prompt
    full_messages = [{"role": "system", "content": chatbot.system_prompt}]
    full_messages.extend(messages)
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=full_messages,
        max_tokens=150
    )
    
    return jsonify({'response': response.choices[0].message.content})
"""

# Setup Instructions:
# 1. Sign up at https://platform.openai.com/
# 2. Get API key from dashboard
# 3. $5 free credit for new accounts
# 4. Cost: ~$0.002 per request (very cheap)
# 5. gpt-3.5-turbo is fastest and cheapest

# Install:
# pip install openai

# Example Questions:
# - "What fertilizer should I use for wheat?"
# - "When should I irrigate my crops?"
# - "How to control aphids organically?"
# - "What is PM-KISAN scheme?"
# - "Best time to sell rice?"
