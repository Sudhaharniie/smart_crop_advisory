import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib

# Disease training data
X = np.array([
    [8,9,2,7,6], [9,8,1,8,5], [7,9,3,6,7],  # Leaf Spot
    [9,2,8,5,7], [8,1,9,4,8], [9,3,9,6,6],  # Bacterial Wilt
    [6,1,1,8,9], [7,2,2,9,8], [5,1,1,7,9],  # Powdery Mildew
    [8,7,3,9,5], [9,8,2,8,6], [7,9,4,9,4],  # Rust
    [9,1,1,2,3], [8,2,2,3,2], [9,1,1,1,4],  # Nitrogen Deficiency
    [2,1,1,1,1], [1,1,1,2,1], [2,2,1,1,2],  # Healthy
])
y = np.array(['Leaf Spot']*3 + ['Bacterial Wilt']*3 + ['Powdery Mildew']*3 + 
             ['Rust Disease']*3 + ['Nitrogen Deficiency']*3 + ['Healthy']*3)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)
joblib.dump(model, 'disease_model.pkl')
print(f"Model trained! Accuracy: {model.score(X, y)*100:.1f}%")
