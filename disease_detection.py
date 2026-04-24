"""
Disease Detection Service
Handles plant disease detection from images
"""
import os
import logging
import numpy as np
from PIL import Image
import joblib

logger = logging.getLogger(__name__)

# Try to import TensorFlow/Keras
try:
    import tensorflow as tf
    from tensorflow import keras
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False
    logger.warning("TensorFlow not installed. Using fallback disease detection.")

class DiseaseDetector:
    def __init__(self):
        self.model = None
        self.class_names = [
            'Healthy',
            'Bacterial Blight',
            'Blast',
            'Brown Spot',
            'Tungro',
            'Leaf Spot',
            'Bacterial Wilt',
            'Powdery Mildew',
            'Rust Disease',
            'Early Blight',
            'Late Blight',
            'Leaf Curl',
            'Mosaic Virus',
            'Anthracnose',
            'Septoria Leaf Spot'
        ]
        
        self.treatments = {
            'Healthy': 'No treatment needed. Continue regular monitoring and good agricultural practices.',
            'Bacterial Blight': 'Apply copper-based bactericide. Remove infected leaves. Improve field drainage.',
            'Blast': 'Apply Tricyclazole or Carbendazim fungicide. Ensure proper spacing between plants.',
            'Brown Spot': 'Apply Mancozeb fungicide. Maintain balanced fertilization, especially potassium.',
            'Tungro': 'Control leafhopper vectors with insecticides. Remove infected plants immediately.',
            'Leaf Spot': 'Apply copper fungicide. Remove infected leaves. Improve air circulation.',
            'Bacterial Wilt': 'Remove and destroy infected plants. Improve soil drainage. Use resistant varieties.',
            'Powdery Mildew': 'Apply sulfur-based fungicide. Increase air circulation. Reduce humidity.',
            'Rust Disease': 'Apply Mancozeb or Propiconazole. Remove infected parts. Avoid overhead irrigation.',
            'Early Blight': 'Apply Chlorothalonil fungicide. Practice crop rotation. Remove plant debris.',
            'Late Blight': 'Apply Metalaxyl or Mancozeb. Improve drainage. Use resistant varieties.',
            'Leaf Curl': 'Control aphid vectors. Apply neem oil. Remove severely infected leaves.',
            'Mosaic Virus': 'Control aphid and whitefly vectors. Remove infected plants. Use virus-free seeds.',
            'Anthracnose': 'Apply copper fungicide. Improve air circulation. Avoid overhead watering.',
            'Septoria Leaf Spot': 'Apply fungicide containing Chlorothalonil. Remove infected leaves. Practice crop rotation.'
        }
        
        self.load_model()
    
    def load_model(self):
        """Load disease detection model"""
        try:
            # Try to load sklearn model (YOU HAVE THIS!)
            if os.path.exists('disease_model.pkl'):
                self.model = joblib.load('disease_model.pkl')
                # Update class names from the model
                if hasattr(self.model, 'classes_'):
                    self.class_names = list(self.model.classes_)
                logger.info(f"Disease detection model loaded with {len(self.class_names)} classes")
                logger.info(f"Classes: {self.class_names}")
                return
            
            # Try to load TensorFlow model
            if TF_AVAILABLE and os.path.exists('disease_detection_model.h5'):
                self.model = keras.models.load_model('disease_detection_model.h5')
                logger.info("TensorFlow disease detection model loaded")
                return
            
            logger.warning("No disease detection model found. Using rule-based detection.")
        
        except Exception as e:
            logger.error(f"Failed to load disease model: {e}")
            self.model = None
    
    def preprocess_image(self, image_path, target_size=(224, 224)):
        """Preprocess image for model input"""
        try:
            img = Image.open(image_path)
            
            # Convert to RGB if needed
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Resize
            img = img.resize(target_size)
            
            # Convert to array
            img_array = np.array(img)
            
            # Normalize
            img_array = img_array / 255.0
            
            # Add batch dimension
            img_array = np.expand_dims(img_array, axis=0)
            
            return img_array
        
        except Exception as e:
            logger.error(f"Failed to preprocess image: {e}")
            return None
    
    def extract_features_from_image(self, image_path):
        """Extract numerical features from image for sklearn model"""
        try:
            img = Image.open(image_path)
            img_array = np.array(img.resize((224, 224)))
            
            # Extract color features
            mean_color = np.mean(img_array, axis=(0, 1))
            std_color = np.std(img_array, axis=(0, 1))
            
            # Extract texture features
            gray = np.mean(img_array, axis=2)
            texture_variance = np.var(gray)
            
            # Create feature vector (5 features for the model)
            features = [
                mean_color[0] / 255.0,  # Red channel mean
                mean_color[1] / 255.0,  # Green channel mean
                mean_color[2] / 255.0,  # Blue channel mean
                np.mean(std_color) / 255.0,  # Color variance
                texture_variance / 10000.0  # Texture variance
            ]
            
            return np.array([features])
        
        except Exception as e:
            logger.error(f"Failed to extract features: {e}")
            return None
    
    def analyze_image_features_fallback(self, image_path):
        """Fallback rule-based detection when ML model not available"""
        try:
            img = Image.open(image_path)
            img_array = np.array(img)
            
            # Calculate color statistics
            mean_color = np.mean(img_array, axis=(0, 1))
            std_color = np.std(img_array, axis=(0, 1))
            
            # Simple heuristics
            green_ratio = mean_color[1] / (mean_color[0] + mean_color[2] + 1)
            color_variance = np.mean(std_color)
            
            # Rule-based detection
            if green_ratio > 1.2 and color_variance < 30:
                return 'Healthy', 0.85
            elif mean_color[0] > mean_color[1] and mean_color[0] > mean_color[2]:
                return 'Rust Disease', 0.72
            elif color_variance > 50:
                return 'Leaf Spot', 0.68
            elif green_ratio < 0.8:
                return 'Bacterial Wilt', 0.65
            else:
                return 'Powdery Mildew', 0.60
        
        except Exception as e:
            logger.error(f"Failed to analyze image: {e}")
            return 'Unknown', 0.0
    
    def detect_disease(self, image_path):
        """
        Detect disease from plant image using REAL ML MODEL
        
        Args:
            image_path (str): Path to the image file
            
        Returns:
            dict: Detection results
        """
        try:
            if self.model is not None:
                # Check if it's sklearn model
                if hasattr(self.model, 'predict_proba'):
                    # Use sklearn model (YOUR TRAINED MODEL!)
                    logger.info("Using trained sklearn disease model")
                    
                    # Extract features from image
                    features = self.extract_features_from_image(image_path)
                    if features is None:
                        raise Exception("Failed to extract features from image")
                    
                    # Predict using REAL ML model
                    predictions = self.model.predict_proba(features)
                    predicted_class = np.argmax(predictions[0])
                    confidence = float(predictions[0][predicted_class]) * 100
                    
                    disease_name = self.class_names[predicted_class]
                    logger.info(f"ML Prediction: {disease_name} with {confidence:.2f}% confidence")
                
                elif TF_AVAILABLE:
                    # Use TensorFlow model
                    logger.info("Using TensorFlow disease model")
                    img_array = self.preprocess_image(image_path)
                    if img_array is None:
                        raise Exception("Failed to preprocess image")
                    
                    predictions = self.model.predict(img_array)
                    predicted_class = np.argmax(predictions[0])
                    confidence = float(predictions[0][predicted_class]) * 100
                    
                    disease_name = self.class_names[predicted_class]
                
                else:
                    raise Exception("Model type not supported")
            
            else:
                # Fallback: Use rule-based detection
                logger.warning("No ML model available, using rule-based detection")
                disease_name, confidence_ratio = self.analyze_image_features_fallback(image_path)
                confidence = confidence_ratio * 100
            
            # Get severity based on confidence
            if confidence > 80:
                severity = 'high'
            elif confidence > 60:
                severity = 'medium'
            else:
                severity = 'low'
            
            # Get treatment
            treatment = self.treatments.get(disease_name, 'Consult agricultural expert for proper diagnosis and treatment.')
            
            return {
                'success': True,
                'disease': disease_name,
                'confidence': round(confidence, 2),
                'severity': severity,
                'treatment': treatment,
                'recommendations': self.get_recommendations(disease_name),
                'model_used': 'ML' if self.model is not None else 'Rule-based'
            }
        
        except Exception as e:
            logger.error(f"Disease detection failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to detect disease. Please try again with a clearer image.'
            }
    
    def get_recommendations(self, disease_name):
        """Get additional recommendations for disease management"""
        general_recommendations = [
            'Monitor your crops regularly for early detection',
            'Maintain proper field hygiene',
            'Use disease-resistant varieties when available',
            'Practice crop rotation',
            'Ensure proper spacing between plants'
        ]
        
        specific_recommendations = {
            'Bacterial Blight': ['Avoid overhead irrigation', 'Use copper-based sprays', 'Remove infected plant parts'],
            'Blast': ['Apply silicon fertilizers', 'Avoid excessive nitrogen', 'Drain fields periodically'],
            'Brown Spot': ['Balance NPK fertilization', 'Improve soil health', 'Use seed treatment'],
            'Rust Disease': ['Apply fungicides at first sign', 'Remove alternate hosts', 'Use resistant varieties'],
            'Powdery Mildew': ['Reduce humidity', 'Improve air circulation', 'Apply sulfur sprays']
        }
        
        return specific_recommendations.get(disease_name, general_recommendations)

# Initialize global disease detector
disease_detector = DiseaseDetector()
