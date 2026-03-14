import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

# Comprehensive crop recommendation training data
# Features: N, P, K, temperature, humidity, ph, rainfall
crop_data = {
    'rice': [[90, 42, 43, 20, 80, 6.5, 200], [85, 40, 40, 22, 82, 6.8, 210], [95, 45, 45, 21, 85, 6.6, 220]],
    'wheat': [[50, 30, 30, 15, 65, 6.8, 50], [55, 32, 32, 16, 68, 7.0, 55], [52, 31, 31, 14, 67, 6.9, 52]],
    'maize': [[80, 40, 20, 25, 70, 6.5, 80], [85, 42, 22, 26, 72, 6.7, 85], [82, 41, 21, 24, 71, 6.6, 82]],
    'cotton': [[120, 40, 40, 28, 60, 7.0, 70], [125, 42, 42, 29, 62, 7.2, 75], [122, 41, 41, 27, 61, 7.1, 72]],
    'sugarcane': [[100, 50, 50, 30, 75, 6.5, 150], [105, 52, 52, 31, 77, 6.7, 155], [102, 51, 51, 29, 76, 6.6, 152]],
    'chickpea': [[40, 60, 80, 20, 65, 7.0, 60], [42, 62, 82, 21, 67, 7.2, 65], [41, 61, 81, 19, 66, 7.1, 62]],
    'kidneybeans': [[20, 60, 20, 22, 70, 6.5, 100], [22, 62, 22, 23, 72, 6.7, 105], [21, 61, 21, 21, 71, 6.6, 102]],
    'pigeonpeas': [[20, 60, 60, 27, 65, 6.0, 100], [22, 62, 62, 28, 67, 6.2, 105], [21, 61, 61, 26, 66, 6.1, 102]],
    'mungbean': [[20, 40, 20, 28, 75, 6.5, 80], [22, 42, 22, 29, 77, 6.7, 85], [21, 41, 21, 27, 76, 6.6, 82]],
    'blackgram': [[40, 60, 20, 30, 70, 7.0, 70], [42, 62, 22, 31, 72, 7.2, 75], [41, 61, 21, 29, 71, 7.1, 72]],
    'lentil': [[20, 60, 20, 18, 65, 6.5, 60], [22, 62, 22, 19, 67, 6.7, 65], [21, 61, 21, 17, 66, 6.6, 62]],
    'pomegranate': [[20, 20, 30, 25, 60, 6.5, 50], [22, 22, 32, 26, 62, 6.7, 55], [21, 21, 31, 24, 61, 6.6, 52]],
    'banana': [[100, 75, 50, 27, 80, 6.5, 100], [105, 77, 52, 28, 82, 6.7, 105], [102, 76, 51, 26, 81, 6.6, 102]],
    'mango': [[20, 20, 30, 30, 70, 6.5, 100], [22, 22, 32, 31, 72, 6.7, 105], [21, 21, 31, 29, 71, 6.6, 102]],
    'grapes': [[20, 125, 200, 25, 70, 6.5, 80], [22, 127, 202, 26, 72, 6.7, 85], [21, 126, 201, 24, 71, 6.6, 82]],
    'watermelon': [[100, 10, 50, 28, 75, 6.5, 50], [105, 12, 52, 29, 77, 6.7, 55], [102, 11, 51, 27, 76, 6.6, 52]],
    'muskmelon': [[100, 10, 50, 30, 70, 6.5, 40], [105, 12, 52, 31, 72, 6.7, 45], [102, 11, 51, 29, 71, 6.6, 42]],
    'apple': [[20, 125, 200, 18, 70, 6.5, 100], [22, 127, 202, 19, 72, 6.7, 105], [21, 126, 201, 17, 71, 6.6, 102]],
    'orange': [[20, 10, 10, 25, 70, 6.5, 100], [22, 12, 12, 26, 72, 6.7, 105], [21, 11, 11, 24, 71, 6.6, 102]],
    'papaya': [[50, 50, 50, 28, 75, 6.5, 100], [52, 52, 52, 29, 77, 6.7, 105], [51, 51, 51, 27, 76, 6.6, 102]],
    'coconut': [[20, 10, 30, 30, 80, 6.5, 150], [22, 12, 32, 31, 82, 6.7, 155], [21, 11, 31, 29, 81, 6.6, 152]],
    'jute': [[80, 40, 40, 28, 80, 6.5, 150], [85, 42, 42, 29, 82, 6.7, 155], [82, 41, 41, 27, 81, 6.6, 152]],
    'coffee': [[100, 20, 30, 23, 70, 6.5, 150], [105, 22, 32, 24, 72, 6.7, 155], [102, 21, 31, 22, 71, 6.6, 152]],
}

# Generate training data with variations
X_train = []
y_train = []

for crop, samples in crop_data.items():
    for sample in samples:
        # Add original sample
        X_train.append(sample)
        y_train.append(crop)
        
        # Add variations (±10% for better generalization)
        for _ in range(5):
            variation = [val * np.random.uniform(0.9, 1.1) for val in sample]
            X_train.append(variation)
            y_train.append(crop)

X_train = np.array(X_train)
y_train = np.array(y_train)

# Train model with optimized parameters
model = RandomForestClassifier(
    n_estimators=200,
    max_depth=15,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    class_weight='balanced'
)

model.fit(X_train, y_train)

# Save model
joblib.dump(model, 'model.pkl')

# Test accuracy
accuracy = model.score(X_train, y_train) * 100
print(f"[OK] Crop Recommendation Model trained!")
print(f"[OK] Training Accuracy: {accuracy:.1f}%")
print(f"[OK] Total samples: {len(X_train)}")
print(f"[OK] Crops: {len(crop_data)}")

# Test prediction
test_sample = [[50, 30, 30, 15, 65, 6.8, 50]]
prediction = model.predict(test_sample)
probabilities = model.predict_proba(test_sample)[0]
confidence = max(probabilities) * 100

print(f"\n[TEST] Test Prediction:")
print(f"   Input: N=50, P=30, K=30, Temp=15C, Humidity=65%, pH=6.8, Rainfall=50mm")
print(f"   Predicted Crop: {prediction[0]}")
print(f"   Confidence: {confidence:.1f}%")

# Yield prediction model
print("\n" + "="*50)
print("Training Yield Prediction Model...")

# Yield data: [crop_code, rainfall, fertilizer, pesticide] -> yield
yield_data = []
yield_labels = []

crop_codes = {crop: idx for idx, crop in enumerate(crop_data.keys())}

for crop, code in crop_codes.items():
    base_yields = {
        'rice': 4000, 'wheat': 4500, 'maize': 5000, 'cotton': 2000,
        'sugarcane': 70000, 'chickpea': 2000, 'kidneybeans': 1600,
        'pigeonpeas': 1400, 'mungbean': 1100, 'blackgram': 950,
        'lentil': 1300, 'pomegranate': 10000, 'banana': 32000,
        'mango': 11500, 'grapes': 15000, 'watermelon': 27500,
        'muskmelon': 20000, 'apple': 15000, 'orange': 20000,
        'papaya': 40000, 'coconut': 10000, 'jute': 2500, 'coffee': 1150
    }
    
    base_yield = base_yields.get(crop, 3000)
    
    for _ in range(20):
        rainfall = np.random.uniform(50, 200)
        fertilizer = np.random.uniform(30000, 70000)
        pesticide = np.random.uniform(1000, 3000)
        
        # Calculate yield with variations
        rain_factor = 1.0 + (rainfall - 100) / 500
        fert_factor = 1.0 + (fertilizer - 50000) / 100000
        pest_factor = 1.0 - (pesticide - 2000) / 10000
        
        yield_val = base_yield * rain_factor * fert_factor * pest_factor
        yield_val = max(yield_val * np.random.uniform(0.85, 1.15), base_yield * 0.5)
        
        yield_data.append([code, rainfall, fertilizer, pesticide])
        yield_labels.append(yield_val)

X_yield = np.array(yield_data)
y_yield = np.array(yield_labels)

yield_model = RandomForestClassifier(n_estimators=150, max_depth=12, random_state=42)
# Convert to classification bins for better prediction
y_yield_bins = np.digitize(y_yield, bins=np.percentile(y_yield, [20, 40, 60, 80]))
yield_model.fit(X_yield, y_yield_bins)

joblib.dump(yield_model, 'yield_model.pkl')
print(f"[OK] Yield Prediction Model trained!")
print(f"[OK] Training samples: {len(X_yield)}")

print("\n" + "="*50)
print("[OK] ALL MODELS TRAINED SUCCESSFULLY!")
print("[OK] Files created: model.pkl, yield_model.pkl")
