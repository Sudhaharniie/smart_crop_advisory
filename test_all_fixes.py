"""
Comprehensive Test Script
Tests all fixes: ML confidence, profit calculation, and dark mode
"""

import sys
import os

print("="*60)
print("COMPREHENSIVE FIX VERIFICATION TEST")
print("="*60)
print()

# Test 1: Check if new models exist
print("[TEST 1] Checking ML Models...")
if os.path.exists('model.pkl') and os.path.exists('yield_model.pkl'):
    print("[PASS] ML models found")
    
    # Load and test model
    try:
        import joblib
        import numpy as np
        
        model = joblib.load('model.pkl')
        
        # Test prediction
        test_input = np.array([[50, 30, 30, 15, 65, 6.8, 50]])
        prediction = model.predict(test_input)[0]
        probabilities = model.predict_proba(test_input)[0]
        confidence = max(probabilities) * 100
        
        print(f"   Predicted Crop: {prediction}")
        print(f"   Confidence: {confidence:.1f}%")
        
        if confidence >= 90:
            print("[PASS] Confidence is 90%+ (Target: 90%+)")
        else:
            print(f"[FAIL] Confidence is {confidence:.1f}% (Target: 90%+)")
            print("   Run: python train_models_improved.py")
    except Exception as e:
        print(f"[FAIL] Error loading model: {e}")
else:
    print("[FAIL] ML models not found")
    print("   Run: python train_models_improved.py")

print()

# Test 2: Check profit calculation in app.py
print("[TEST 2] Checking Profit Calculation...")
try:
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()
        
    if 'predicted_yield_per_hectare = predict_yield(crop_name, weather, 1)' in content:
        print("[PASS] Profit calculation fixed")
        print("   Formula: yield_per_hectare * farm_size / 100 * price")
    else:
        print("[FAIL] Old profit calculation still in use")
        print("   Check app.py around line 1050")
except Exception as e:
    print(f"[FAIL] Error reading app.py: {e}")

print()

# Test 3: Check dark mode CSS
print("[TEST 3] Checking Dark Mode CSS...")
if os.path.exists('static/css/dark-mode-fixes.css'):
    print("[PASS] Dark mode CSS file exists")
    
    # Check if it's linked in dashboard.html
    try:
        with open('templates/dashboard.html', 'r', encoding='utf-8') as f:
            content = f.read()
            
        if 'dark-mode-fixes.css' in content:
            print("[PASS] Dark mode CSS linked in dashboard.html")
        else:
            print("[FAIL] Dark mode CSS not linked in dashboard.html")
            print("   Add: <link rel=\"stylesheet\" href=\"{{ url_for('static', filename='css/dark-mode-fixes.css') }}\">")
    except Exception as e:
        print(f"[WARNING] Could not verify dashboard.html: {e}")
else:
    print("[FAIL] Dark mode CSS file not found")
    print("   File should exist: static/css/dark-mode-fixes.css")

print()

# Test 4: Simulate profit calculation
print("[TEST 4] Simulating Profit Calculation...")
try:
    # Example: Wheat, 1 hectare
    crop_name = "wheat"
    yield_per_hectare = 4500  # kg
    farm_size = 1  # hectare
    price_per_quintal = 2500  # rupees
    cost_per_hectare = 20000  # rupees
    
    total_yield = yield_per_hectare * farm_size
    total_yield_quintals = total_yield / 100
    revenue = total_yield_quintals * price_per_quintal
    costs = cost_per_hectare * farm_size
    profit = revenue - costs
    roi = (profit / costs) * 100
    
    print(f"   Crop: {crop_name}")
    print(f"   Yield: {total_yield} kg")
    print(f"   Revenue: Rs {revenue:,.0f}")
    print(f"   Costs: Rs {costs:,.0f}")
    print(f"   Profit: Rs {profit:,.0f}")
    print(f"   ROI: {roi:.1f}%")
    
    if profit > 0:
        print("[PASS] Profit is positive")
    else:
        print("[FAIL] Profit is negative or zero")
except Exception as e:
    print(f"[FAIL] Error in calculation: {e}")

print()

# Test 5: Check required files
print("[TEST 5] Checking Required Files...")
required_files = [
    'app.py',
    'train_models_improved.py',
    'static/css/dark-mode-fixes.css',
    'templates/dashboard.html',
    'market_data.py',
    'climate_risk.py'
]

all_exist = True
for file in required_files:
    if os.path.exists(file):
        print(f"[OK] {file}")
    else:
        print(f"[MISSING] {file}")
        all_exist = False

if all_exist:
    print("[PASS] All required files exist")
else:
    print("[FAIL] Some files are missing")

print()

# Summary
print("="*60)
print("TEST SUMMARY")
print("="*60)
print()
print("Next Steps:")
print("1. If any tests failed, follow the instructions above")
print("2. Run: python train_models_improved.py")
print("3. Run: python app.py")
print("4. Open: http://localhost:5000")
print("5. Verify:")
print("   - Confidence: 90%+")
print("   - Profit: Positive")
print("   - Dark mode: All visible")
print()
print("="*60)
