"""
ML-Based Irrigation Prediction System
Predicts irrigation needs using machine learning
"""

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import joblib
import os
import logging

logger = logging.getLogger(__name__)

class IrrigationPredictor:
    """ML-based irrigation prediction"""
    
    def __init__(self):
        self.model = None
        self.scaler = None
        self.load_or_train_model()
    
    def load_or_train_model(self):
        """Load existing model or train new one"""
        model_path = 'irrigation_model.pkl'
        scaler_path = 'irrigation_scaler.pkl'
        
        if os.path.exists(model_path) and os.path.exists(scaler_path):
            try:
                self.model = joblib.load(model_path)
                self.scaler = joblib.load(scaler_path)
                logger.info("Irrigation model loaded successfully")
                return
            except Exception as e:
                logger.warning(f"Failed to load model: {e}")
        
        # Train new model with synthetic data
        self.train_model()
    
    def train_model(self):
        """Train irrigation prediction model"""
        logger.info("Training irrigation prediction model...")
        
        # Generate synthetic training data
        np.random.seed(42)
        n_samples = 1000
        
        # Features: soil_moisture, temperature, humidity, rainfall, crop_water_need
        X = []
        y = []
        
        for _ in range(n_samples):
            soil_moisture = np.random.uniform(20, 90)
            temperature = np.random.uniform(15, 45)
            humidity = np.random.uniform(30, 95)
            rainfall = np.random.uniform(0, 50)
            crop_water_need = np.random.uniform(3, 8)  # mm/day
            
            # Decision logic for irrigation need
            # 0 = No irrigation, 1 = Light irrigation, 2 = Heavy irrigation
            if soil_moisture > 70 or rainfall > 20:
                irrigation_need = 0  # No irrigation
            elif soil_moisture > 50 and temperature < 30:
                irrigation_need = 1  # Light irrigation
            elif soil_moisture < 40 or (temperature > 35 and humidity < 40):
                irrigation_need = 2  # Heavy irrigation
            else:
                irrigation_need = 1  # Light irrigation
            
            X.append([soil_moisture, temperature, humidity, rainfall, crop_water_need])
            y.append(irrigation_need)
        
        X = np.array(X)
        y = np.array(y)
        
        # Scale features
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)
        
        # Train Random Forest
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self.model.fit(X_scaled, y)
        
        # Save model
        joblib.dump(self.model, 'irrigation_model.pkl')
        joblib.dump(self.scaler, 'irrigation_scaler.pkl')
        
        # Calculate accuracy
        accuracy = self.model.score(X_scaled, y)
        logger.info(f"Irrigation model trained with accuracy: {accuracy*100:.2f}%")
    
    def predict_irrigation(self, soil_moisture, temperature, humidity, rainfall, crop_type='general'):
        """
        Predict irrigation needs
        
        Args:
            soil_moisture: Current soil moisture (%)
            temperature: Temperature (°C)
            humidity: Humidity (%)
            rainfall: Recent rainfall (mm)
            crop_type: Type of crop
            
        Returns:
            dict: Irrigation prediction with recommendation
        """
        
        # Crop water requirements (mm/day)
        crop_water_needs = {
            'rice': 7.5,
            'wheat': 4.5,
            'maize': 5.0,
            'cotton': 6.0,
            'sugarcane': 8.0,
            'vegetables': 5.5,
            'general': 5.0
        }
        
        crop_water_need = crop_water_needs.get(crop_type.lower(), 5.0)
        
        # Prepare features
        features = np.array([[
            soil_moisture,
            temperature,
            humidity,
            rainfall,
            crop_water_need
        ]])
        
        # Scale features
        features_scaled = self.scaler.transform(features)
        
        # Predict
        prediction = self.model.predict(features_scaled)[0]
        probabilities = self.model.predict_proba(features_scaled)[0]
        confidence = max(probabilities) * 100
        
        # Get feature importance
        feature_names = ['Soil Moisture', 'Temperature', 'Humidity', 'Rainfall', 'Crop Water Need']
        importances = self.model.feature_importances_
        
        # Map prediction to recommendation
        irrigation_levels = {
            0: {
                'level': 'No Irrigation Needed',
                'amount': '0 mm',
                'frequency': 'Skip today',
                'reason': 'Soil moisture adequate or recent rainfall',
                'color': '#10b981',
                'icon': '✅'
            },
            1: {
                'level': 'Light Irrigation',
                'amount': '15-20 mm',
                'frequency': 'Once every 2-3 days',
                'reason': 'Moderate soil moisture, normal conditions',
                'color': '#f59e0b',
                'icon': '💧'
            },
            2: {
                'level': 'Heavy Irrigation',
                'amount': '30-40 mm',
                'frequency': 'Daily',
                'reason': 'Low soil moisture or high temperature stress',
                'color': '#ef4444',
                'icon': '🚨'
            }
        }
        
        result = irrigation_levels[prediction]
        
        # Add timing recommendation
        if prediction > 0:
            if temperature > 30:
                timing = 'Early morning (5-7 AM) or evening (6-8 PM)'
            else:
                timing = 'Morning (6-9 AM)'
        else:
            timing = 'Not required'
        
        # Calculate water volume for farm
        water_per_hectare = {0: 0, 1: 17.5, 2: 35}  # mm
        
        return {
            'prediction': prediction,
            'confidence': round(confidence, 2),
            'level': result['level'],
            'amount': result['amount'],
            'frequency': result['frequency'],
            'reason': result['reason'],
            'timing': timing,
            'color': result['color'],
            'icon': result['icon'],
            'water_per_hectare_mm': water_per_hectare[prediction],
            'method': 'Drip irrigation recommended' if prediction > 0 else 'No irrigation',
            'feature_importance': {
                feature_names[i]: round(importances[i] * 100, 1)
                for i in range(len(feature_names))
            },
            'factors': self._get_key_factors(soil_moisture, temperature, humidity, rainfall)
        }
    
    def _get_key_factors(self, soil_moisture, temperature, humidity, rainfall):
        """Identify key factors affecting irrigation decision"""
        factors = []
        
        if soil_moisture < 40:
            factors.append(f"⚠️ Low soil moisture ({soil_moisture}%)")
        elif soil_moisture > 70:
            factors.append(f"✅ High soil moisture ({soil_moisture}%)")
        
        if temperature > 35:
            factors.append(f"🌡️ High temperature ({temperature}°C)")
        
        if humidity < 40:
            factors.append(f"💨 Low humidity ({humidity}%)")
        
        if rainfall > 10:
            factors.append(f"🌧️ Recent rainfall ({rainfall}mm)")
        
        return factors

# Global instance
irrigation_predictor = IrrigationPredictor()

def predict_irrigation_ml(soil_moisture, temperature, humidity, rainfall, crop_type='general'):
    """Predict irrigation needs using ML"""
    return irrigation_predictor.predict_irrigation(
        soil_moisture, temperature, humidity, rainfall, crop_type
    )
