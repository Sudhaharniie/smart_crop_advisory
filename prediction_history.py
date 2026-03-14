"""
Prediction History Tracking
Store and retrieve all crop predictions
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# Add this model to your app.py database models

class PredictionHistory(db.Model):
    """Store all crop prediction history"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Input parameters
    location = db.Column(db.String(100))
    nitrogen = db.Column(db.Float)
    phosphorus = db.Column(db.Float)
    potassium = db.Column(db.Float)
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)
    ph = db.Column(db.Float)
    rainfall = db.Column(db.Float)
    
    # Predictions
    recommended_crop_1 = db.Column(db.String(50))
    confidence_1 = db.Column(db.Float)
    recommended_crop_2 = db.Column(db.String(50))
    confidence_2 = db.Column(db.Float)
    recommended_crop_3 = db.Column(db.String(50))
    confidence_3 = db.Column(db.Float)
    
    # Results
    predicted_yield = db.Column(db.Float)
    estimated_profit = db.Column(db.Float)
    
    # Metadata
    prediction_date = db.Column(db.DateTime, default=datetime.utcnow)
    season = db.Column(db.String(20))
    
    def to_dict(self):
        return {
            'id': self.id,
            'date': self.prediction_date.strftime('%B %d, %Y'),
            'location': self.location,
            'top_crop': self.recommended_crop_1,
            'confidence': self.confidence_1,
            'yield': self.predicted_yield,
            'profit': self.estimated_profit,
            'season': self.season,
            'soil_params': {
                'N': self.nitrogen,
                'P': self.phosphorus,
                'K': self.potassium,
                'pH': self.ph
            }
        }

def save_prediction(user_id, soil_data, weather, top_3_crops, predicted_yield, estimated_profit):
    """Save prediction to history"""
    try:
        # Determine season
        month = datetime.now().month
        if 6 <= month <= 10:
            season = 'Kharif'
        elif 11 <= month or month <= 3:
            season = 'Rabi'
        else:
            season = 'Zaid'
        
        prediction = PredictionHistory(
            user_id=user_id,
            location=db.session.get(User, user_id).location,
            nitrogen=soil_data['nitrogen'],
            phosphorus=soil_data['phosphorus'],
            potassium=soil_data['potassium'],
            temperature=weather['temperature'],
            humidity=weather['humidity'],
            ph=soil_data['ph'],
            rainfall=weather['rainfall'],
            recommended_crop_1=top_3_crops[0]['crop'],
            confidence_1=top_3_crops[0]['confidence'],
            recommended_crop_2=top_3_crops[1]['crop'] if len(top_3_crops) > 1 else None,
            confidence_2=top_3_crops[1]['confidence'] if len(top_3_crops) > 1 else None,
            recommended_crop_3=top_3_crops[2]['crop'] if len(top_3_crops) > 2 else None,
            confidence_3=top_3_crops[2]['confidence'] if len(top_3_crops) > 2 else None,
            predicted_yield=predicted_yield,
            estimated_profit=estimated_profit,
            season=season
        )
        
        db.session.add(prediction)
        db.session.commit()
        
        return True
    except Exception as e:
        logger.error(f"Failed to save prediction: {e}")
        return False

def get_user_prediction_history(user_id, limit=10):
    """Get user's prediction history"""
    try:
        predictions = PredictionHistory.query.filter_by(user_id=user_id)\
            .order_by(PredictionHistory.prediction_date.desc())\
            .limit(limit).all()
        
        return [p.to_dict() for p in predictions]
    except Exception as e:
        logger.error(f"Failed to get prediction history: {e}")
        return []

def get_prediction_statistics(user_id):
    """Get statistics from prediction history"""
    try:
        predictions = PredictionHistory.query.filter_by(user_id=user_id).all()
        
        if not predictions:
            return None
        
        # Most recommended crops
        crop_counts = {}
        for p in predictions:
            crop = p.recommended_crop_1
            crop_counts[crop] = crop_counts.get(crop, 0) + 1
        
        most_recommended = sorted(crop_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        
        # Average metrics
        avg_yield = sum(p.predicted_yield for p in predictions) / len(predictions)
        avg_profit = sum(p.estimated_profit for p in predictions) / len(predictions)
        
        # Season distribution
        season_counts = {}
        for p in predictions:
            season_counts[p.season] = season_counts.get(p.season, 0) + 1
        
        return {
            'total_predictions': len(predictions),
            'most_recommended_crops': most_recommended,
            'average_yield': round(avg_yield, 2),
            'average_profit': round(avg_profit, 2),
            'season_distribution': season_counts,
            'first_prediction': predictions[-1].prediction_date.strftime('%B %Y'),
            'latest_prediction': predictions[0].prediction_date.strftime('%B %Y')
        }
    except Exception as e:
        logger.error(f"Failed to get statistics: {e}")
        return None
