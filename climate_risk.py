"""
Climate Risk Assessment Module
Provides real-time climate risk analysis based on weather data
"""

import logging

logger = logging.getLogger(__name__)

def get_climate_risk_assessment(location, forecast_data):
    """
    Calculate comprehensive climate risk assessment
    
    Args:
        location: User location
        forecast_data: Weather forecast data from API
        
    Returns:
        dict: Climate risk assessment with drought, flood, heat, frost risks
    """
    try:
        # Safely extract forecast list
        forecast_list = forecast_data.get('list', [])
        
        if not forecast_list or len(forecast_list) == 0:
            logger.warning(f"No forecast data available for {location}")
            return get_default_climate_risk()
        
        # Extract temperature and rainfall data safely
        temps = []
        rainfall = []
        
        for item in forecast_list[:7]:  # 7-day forecast
            if isinstance(item, dict):
                # Temperature
                if 'temp' in item:
                    temps.append(item['temp'])
                elif 'main' in item and 'temp' in item['main']:
                    temps.append(item['main']['temp'])
                
                # Rainfall
                if 'rain' in item:
                    rainfall.append(item.get('rain', 0))
                else:
                    rainfall.append(0)
        
        # Fallback if no data extracted
        if not temps:
            temps = [25, 26, 24, 27, 25, 26, 25]
        if not rainfall:
            rainfall = [0, 0, 2, 0, 1, 0, 0]
        
        # Calculate statistics
        total_rainfall = sum(rainfall)
        avg_rainfall = total_rainfall / len(rainfall) if rainfall else 0
        max_temp = max(temps) if temps else 25
        min_temp = min(temps) if temps else 15
        
        # Drought Risk
        if total_rainfall < 5:
            drought = {'level': 'Critical', 'value': total_rainfall, 'description': 'Severe drought conditions'}
        elif total_rainfall < 15:
            drought = {'level': 'High', 'value': total_rainfall, 'description': 'High drought risk'}
        elif total_rainfall < 30:
            drought = {'level': 'Medium', 'value': total_rainfall, 'description': 'Moderate drought risk'}
        else:
            drought = {'level': 'Low', 'value': total_rainfall, 'description': 'Low drought risk'}
        
        # Flood Risk
        if total_rainfall > 150:
            flood = {'level': 'Critical', 'value': total_rainfall, 'description': 'Severe flood risk'}
        elif total_rainfall > 100:
            flood = {'level': 'High', 'value': total_rainfall, 'description': 'High flood risk'}
        elif total_rainfall > 50:
            flood = {'level': 'Medium', 'value': total_rainfall, 'description': 'Moderate rainfall'}
        else:
            flood = {'level': 'Low', 'value': total_rainfall, 'description': 'Low flood risk'}
        
        # Heat Stress
        if max_temp > 42:
            heat_stress = {'level': 'Critical', 'value': max_temp, 'description': 'Extreme heat stress'}
        elif max_temp > 38:
            heat_stress = {'level': 'High', 'value': max_temp, 'description': 'High heat stress'}
        elif max_temp > 35:
            heat_stress = {'level': 'Medium', 'value': max_temp, 'description': 'Moderate heat'}
        else:
            heat_stress = {'level': 'Low', 'value': max_temp, 'description': 'Normal temperature'}
        
        # Frost Risk
        if min_temp < 5:
            frost = {'level': 'Critical', 'value': min_temp, 'description': 'Frost risk'}
        elif min_temp < 10:
            frost = {'level': 'High', 'value': min_temp, 'description': 'Cold stress risk'}
        elif min_temp < 15:
            frost = {'level': 'Medium', 'value': min_temp, 'description': 'Cool temperatures'}
        else:
            frost = {'level': 'Low', 'value': min_temp, 'description': 'Temperature suitable'}
        
        # Overall Risk Score
        risk_scores = {
            'Critical': 90,
            'High': 75,
            'Medium': 50,
            'Low': 20
        }
        
        overall_score = max(
            risk_scores[drought['level']],
            risk_scores[flood['level']],
            risk_scores[heat_stress['level']],
            risk_scores[frost['level']]
        )
        
        if overall_score >= 75:
            overall_risk = 'Critical'
        elif overall_score >= 50:
            overall_risk = 'High'
        elif overall_score >= 30:
            overall_risk = 'Medium'
        else:
            overall_risk = 'Low'
        
        # Recommendations
        recommendations = []
        alerts = []
        
        if drought['level'] in ['Critical', 'High']:
            recommendations.append('Implement water conservation measures immediately')
            recommendations.append('Use drip irrigation to save water')
            alerts.append('DROUGHT ALERT: Plan irrigation schedule carefully')
        
        if flood['level'] in ['Critical', 'High']:
            recommendations.append('Ensure proper drainage systems')
            recommendations.append('Avoid planting in low-lying areas')
            alerts.append('FLOOD ALERT: Heavy rainfall expected')
        
        if heat_stress['level'] in ['Critical', 'High']:
            recommendations.append('Increase irrigation frequency')
            recommendations.append('Provide shade for sensitive crops')
            alerts.append('HEAT ALERT: Extreme temperatures expected')
        
        if frost['level'] in ['Critical', 'High']:
            recommendations.append('Protect sensitive crops from frost')
            recommendations.append('Cover young plants overnight')
            alerts.append('FROST ALERT: Cold temperatures expected')
        
        return {
            'drought': drought,
            'flood': flood,
            'heat_stress': heat_stress,
            'frost': frost,
            'overall_risk': overall_risk,
            'risk_score': overall_score,
            'recommendations': recommendations,
            'alerts': alerts
        }
    
    except Exception as e:
        logger.error(f"Climate risk assessment error: {e}")
        return get_default_climate_risk()

def get_default_climate_risk():
    """Return default climate risk when data is unavailable"""
    return {
        'drought': {'level': 'Low', 'value': 20, 'description': 'Normal conditions'},
        'flood': {'level': 'Low', 'value': 20, 'description': 'Normal conditions'},
        'heat_stress': {'level': 'Low', 'value': 25, 'description': 'Normal temperature'},
        'frost': {'level': 'Low', 'value': 15, 'description': 'Normal temperature'},
        'overall_risk': 'Low',
        'risk_score': 20,
        'recommendations': ['Monitor weather conditions regularly'],
        'alerts': []
    }
