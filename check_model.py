import joblib
import numpy as np

print("Testing current model...")
model = joblib.load('model.pkl')

# Test prediction
test_input = np.array([[50, 30, 30, 15, 65, 6.8, 50]])
prediction = model.predict(test_input)[0]
probabilities = model.predict_proba(test_input)[0]
confidence = max(probabilities) * 100

print(f"Predicted Crop: {prediction}")
print(f"Confidence: {confidence:.1f}%")
print(f"Number of classes: {len(model.classes_)}")
print(f"Classes: {model.classes_[:5]}...")  # Show first 5

if confidence >= 90:
    print("\n[OK] Model is the NEW trained model (90%+ confidence)")
else:
    print(f"\n[WARNING] Model is OLD (confidence: {confidence:.1f}%)")
    print("You need to run: python train_models_improved.py")
