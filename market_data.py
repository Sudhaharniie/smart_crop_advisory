# Real Market Prices - Based on Indian Mandi Data
import requests
import os
import logging
from datetime import datetime, timedelta
import json

logger = logging.getLogger(__name__)

CROP_PRICES = {
    'rice': 2000, 'wheat': 2500, 'maize': 1800, 'cotton': 5500, 'sugarcane': 3000,
    'jute': 4200, 'coffee': 6000, 'chickpea': 5000, 'kidneybeans': 8000,
    'pigeonpeas': 6500, 'mothbeans': 5500, 'mungbean': 7000, 'blackgram': 6800,
    'lentil': 7500, 'pomegranate': 8000, 'banana': 2000, 'mango': 4000,
    'grapes': 6000, 'watermelon': 1500, 'muskmelon': 2500, 'apple': 8000,
    'papaya': 2000, 'coconut': 3500, 'orange': 4500
}

def get_real_market_prices():
    """Get REAL market prices from API (NO RANDOM VALUES)"""
    
    # Get API key from environment
    api_key = os.getenv('MANDI_API_KEY') or os.getenv('DATA_GOV_IN_KEY')
    
    if api_key and api_key != 'your_mandi_api_key_here' and api_key != 'your_data_gov_in_key_here':
        try:
            # Try to fetch from data.gov.in Agmarknet API
            logger.info("🔄 Fetching REAL market prices from Mandi API...")
            
            url = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"
            params = {
                'api-key': api_key,
                'format': 'json',
                'limit': 100
            }
            
            response = requests.get(url, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                
                if 'records' in data and len(data['records']) > 0:
                    prices = {}
                    
                    # Process real API data
                    for record in data['records']:
                        commodity = record.get('commodity', '').lower()
                        
                        # Map API commodity names to our crop names
                        commodity_mapping = {
                            'paddy': 'rice',
                            'rice': 'rice',
                            'wheat': 'wheat',
                            'maize': 'maize',
                            'cotton': 'cotton',
                            'sugarcane': 'sugarcane',
                            'gram': 'chickpea',
                            'tur': 'pigeonpeas',
                            'moong': 'mungbean',
                            'urad': 'blackgram'
                        }
                        
                        crop_name = commodity_mapping.get(commodity, commodity)
                        
                        if crop_name in CROP_PRICES:
                            try:
                                modal_price = float(record.get('modal_price', 0))
                                min_price = float(record.get('min_price', 0))
                                max_price = float(record.get('max_price', 0))
                                
                                if modal_price > 0:
                                    # Calculate trend from min/max
                                    avg_price = (min_price + max_price) / 2
                                    if modal_price > avg_price * 1.05:
                                        trend = 'up'
                                    elif modal_price < avg_price * 0.95:
                                        trend = 'down'
                                    else:
                                        trend = 'stable'
                                    
                                    # Estimate last week price (5% variation)
                                    last_week = modal_price * 0.98 if trend == 'up' else modal_price * 1.02 if trend == 'down' else modal_price
                                    
                                    prices[crop_name] = {
                                        'current_price': round(modal_price, 2),
                                        'last_week': round(last_week, 2),
                                        'trend': trend,
                                        'min_price': round(min_price, 2),
                                        'max_price': round(max_price, 2),
                                        'market': record.get('market', 'N/A'),
                                        'date': record.get('arrival_date', datetime.now().strftime('%Y-%m-%d')),
                                        'source': '✅ REAL API'
                                    }
                                    logger.info(f"✅ REAL price for {crop_name}: ₹{modal_price} (from Mandi API)")
                            except (ValueError, TypeError) as e:
                                logger.warning(f"Error parsing price for {commodity}: {e}")
                                continue
                    
                    if prices:
                        logger.info(f"✅ Fetched {len(prices)} REAL market prices from Mandi API")
                        
                        # Fill remaining crops with base prices (marked as estimated)
                        for crop, base_price in CROP_PRICES.items():
                            if crop not in prices:
                                prices[crop] = {
                                    'current_price': base_price,
                                    'last_week': base_price,
                                    'trend': 'stable',
                                    'source': 'base_price'
                                }
                        
                        return prices
                    else:
                        logger.warning("API returned no valid prices, using fallback")
                        return get_fallback_prices()
                else:
                    logger.warning("API response has no records")
                    return get_fallback_prices()
            else:
                logger.error(f"API returned status code: {response.status_code}")
                return get_fallback_prices()
                
        except requests.exceptions.Timeout:
            logger.error("Market API timeout")
            return get_fallback_prices()
        except requests.exceptions.RequestException as e:
            logger.error(f"Market API request failed: {e}")
            return get_fallback_prices()
        except Exception as e:
            logger.error(f"Market API error: {e}")
            return get_fallback_prices()
    else:
        logger.warning("⚠️ No Mandi API key configured. Add MANDI_API_KEY to .env file")
        logger.info("Get your free API key from: https://data.gov.in/")
        return get_fallback_prices()

def get_fallback_prices():
    """Fallback to base prices (NO RANDOM) when API fails"""
    logger.info("Using fallback base prices (no random values)")
    
    prices = {}
    for crop, base_price in CROP_PRICES.items():
        prices[crop] = {
            'current_price': base_price,
            'last_week': base_price,
            'trend': 'stable',
            'source': 'fallback'
        }
    
    return prices
