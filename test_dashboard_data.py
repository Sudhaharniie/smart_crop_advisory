import sys
sys.path.insert(0, 'D:\\agri project new\\project agri')

from app import app, db, User, recommend_crops, predict_yield, get_user_soil_data, get_weather_data, CROP_PRICES
import numpy as np

print("="*60)
print("TESTING DASHBOARD DATA")
print("="*60)

with app.app_context():
    # Get first user
    user = User.query.first()
    if not user:
        print("ERROR: No user found. Please register first.")
        sys.exit(1)
    
    print(f"\n1. USER INFO:")
    print(f"   Username: {user.username}")
    print(f"   Location: {user.location}")
    print(f"   Farm Size: {user.farm_size} hectares")
    
    # Get weather
    print(f"\n2. WEATHER DATA:")
    weather, forecast, forecast_dates = get_weather_data(user.location)
    print(f"   Temperature: {weather['temperature']}°C")
    print(f"   Humidity: {weather['humidity']}%")
    print(f"   Rainfall: {weather['rainfall']}mm")
    
    # Get soil
    print(f"\n3. SOIL DATA:")
    soil_data = get_user_soil_data(user.id)
    print(f"   Nitrogen: {soil_data['nitrogen']}")
    print(f"   Phosphorus: {soil_data['phosphorus']}")
    print(f"   Potassium: {soil_data['potassium']}")
    print(f"   pH: {soil_data['ph']}")
    
    # Get crop recommendations
    print(f"\n4. CROP RECOMMENDATIONS:")
    top_3_crops = recommend_crops(
        soil_data['nitrogen'],
        soil_data['phosphorus'],
        soil_data['potassium'],
        weather['temperature'],
        weather['humidity'],
        soil_data['ph'],
        weather['rainfall']
    )
    
    for i, crop in enumerate(top_3_crops, 1):
        print(f"\n   Crop #{i}: {crop['crop']}")
        print(f"   Confidence: {crop['confidence']}%")
        
        # Calculate profit
        crop_name = crop['crop']
        farm_size = user.farm_size or 1
        
        predicted_yield_per_hectare = predict_yield(crop_name, weather, 1)
        total_yield = predicted_yield_per_hectare * farm_size
        
        price_per_quintal = CROP_PRICES.get(crop_name.lower(), 2500)
        total_yield_in_quintals = total_yield / 100
        revenue = total_yield_in_quintals * price_per_quintal
        
        base_cost_per_hectare = 20000
        estimated_costs = base_cost_per_hectare * farm_size
        
        net_profit = revenue - estimated_costs
        roi = (net_profit / estimated_costs) * 100 if estimated_costs > 0 else 0
        
        print(f"   Yield: {total_yield} kg")
        print(f"   Revenue: Rs {revenue:,.2f}")
        print(f"   Costs: Rs {estimated_costs:,.2f}")
        print(f"   PROFIT: Rs {net_profit:,.2f}")
        print(f"   ROI: {roi:.1f}%")

print("\n" + "="*60)
print("If you see POSITIVE profit above, the code is working!")
print("If dashboard still shows wrong values, it's a browser cache issue.")
print("="*60)
