# PROFIT CALCULATION FIX
# This fixes the negative/zero profit issue

# The problem is in the profit calculation logic in app.py around line 1050-1070
# Current calculation has issues with:
# 1. Wrong formula for revenue calculation
# 2. Costs are too high
# 3. Price per quintal not properly applied

# FIXED CALCULATION:

# OLD (WRONG):
# yield_in_quintals = predicted_yield / 100
# revenue = yield_in_quintals * price * farm_size
# base_cost_per_hectare = 25000
# estimated_costs = base_cost_per_hectare * farm_size

# NEW (CORRECT):
# predicted_yield is already per hectare (e.g., 4000 kg/hectare)
# For 1 hectare farm:
#   - Yield: 4000 kg
#   - Price: ₹2500 per quintal (100kg)
#   - Revenue: (4000/100) * 2500 = 40 quintals * 2500 = ₹100,000
#   - Costs: ₹20,000 (seeds, fertilizer, labor, pesticide)
#   - Profit: ₹100,000 - ₹20,000 = ₹80,000
#   - ROI: (80,000/20,000) * 100 = 400%

# The fix:
# 1. predicted_yield is TOTAL yield for farm (already multiplied by farm_size)
# 2. Convert to quintals: yield_in_quintals = predicted_yield / 100
# 3. Revenue: yield_in_quintals * price_per_quintal
# 4. Costs: base_cost * farm_size (reduced to 20000)
# 5. Profit: revenue - costs

print("Apply this fix to app.py around line 1050:")
print("""
# Calculate yield and profit for each crop with REAL prices from market data
for crop_data in top_3_crops:
    crop_name = crop_data['crop']
    
    # Get farm size
    farm_size = user.farm_size or 1
    
    # Predict yield (returns kg per hectare)
    predicted_yield_per_hectare = predict_yield(crop_name, weather, 1)  # Get per hectare first
    total_yield = predicted_yield_per_hectare * farm_size  # Total for entire farm
    
    # Get REAL market price (per quintal)
    price_per_quintal = CROP_PRICES.get(crop_name.lower(), 2500)
    
    # Calculate revenue
    # Convert kg to quintals (1 quintal = 100 kg)
    total_yield_in_quintals = total_yield / 100
    revenue = total_yield_in_quintals * price_per_quintal
    
    # Calculate costs (realistic)
    base_cost_per_hectare = 20000  # Seeds, fertilizer, pesticide, labor
    estimated_costs = base_cost_per_hectare * farm_size
    
    # Calculate profit
    net_profit = revenue - estimated_costs
    roi = (net_profit / estimated_costs) * 100 if estimated_costs > 0 else 0
    
    # Store in crop_data
    crop_data['yield'] = round(total_yield, 2)
    crop_data['price'] = price_per_quintal
    crop_data['revenue'] = round(revenue, 2)
    crop_data['costs'] = round(estimated_costs, 2)
    crop_data['profit'] = round(net_profit, 2)
    crop_data['roi'] = round(roi, 2)
""")
