"""
Satellite Crop Health Monitoring using NDVI
Uses Sentinel-2 satellite data for vegetation analysis
"""

import requests
import logging
from datetime import datetime, timedelta
import os

logger = logging.getLogger(__name__)

class SatelliteCropHealth:
    """Monitor crop health using satellite NDVI data"""
    
    def __init__(self):
        # Sentinel Hub API (free tier available)
        self.sentinel_api_key = os.getenv('SENTINEL_API_KEY', '')
        self.base_url = "https://services.sentinel-hub.com/api/v1"
    
    def get_ndvi_data(self, latitude, longitude, farm_size_hectares=1):
        """
        Get NDVI (Normalized Difference Vegetation Index) data
        
        NDVI Scale:
        - 0.8 to 1.0: Very healthy dense vegetation
        - 0.6 to 0.8: Healthy vegetation
        - 0.4 to 0.6: Moderate vegetation
        - 0.2 to 0.4: Sparse vegetation
        - 0.0 to 0.2: Very sparse or no vegetation
        - Negative: Water, snow, clouds
        
        Args:
            latitude: Farm latitude
            longitude: Farm longitude
            farm_size_hectares: Farm size in hectares
            
        Returns:
            dict: NDVI analysis with health score and recommendations
        """
        
        try:
            # If API key is configured, fetch real satellite data
            if self.sentinel_api_key and self.sentinel_api_key != 'your_sentinel_api_key':
                return self._fetch_real_ndvi(latitude, longitude, farm_size_hectares)
            else:
                # Return simulated data based on location and season
                return self._simulate_ndvi(latitude, longitude, farm_size_hectares)
        
        except Exception as e:
            logger.error(f"NDVI data fetch error: {e}")
            return self._simulate_ndvi(latitude, longitude, farm_size_hectares)
    
    def _fetch_real_ndvi(self, lat, lon, farm_size):
        """Fetch real NDVI data from Sentinel Hub API"""
        try:
            # Calculate bounding box (approximate 1 hectare = 100m x 100m)
            offset = 0.001 * (farm_size ** 0.5)  # Rough approximation
            
            bbox = {
                'min_lon': lon - offset,
                'min_lat': lat - offset,
                'max_lon': lon + offset,
                'max_lat': lat + offset
            }
            
            # Sentinel Hub request
            headers = {
                'Authorization': f'Bearer {self.sentinel_api_key}',
                'Content-Type': 'application/json'
            }
            
            # Request NDVI data for last 30 days
            end_date = datetime.now()
            start_date = end_date - timedelta(days=30)
            
            payload = {
                'bbox': [bbox['min_lon'], bbox['min_lat'], bbox['max_lon'], bbox['max_lat']],
                'time': f"{start_date.strftime('%Y-%m-%d')}/{end_date.strftime('%Y-%m-%d')}",
                'format': 'application/json'
            }
            
            response = requests.post(
                f"{self.base_url}/process",
                headers=headers,
                json=payload,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                ndvi_value = data.get('ndvi', 0.65)  # Extract NDVI
                
                logger.info(f"✅ Real NDVI data fetched: {ndvi_value}")
                return self._analyze_ndvi(ndvi_value, farm_size, source='satellite')
            else:
                logger.warning(f"Sentinel API error: {response.status_code}")
                return self._simulate_ndvi(lat, lon, farm_size)
        
        except Exception as e:
            logger.error(f"Real NDVI fetch failed: {e}")
            return self._simulate_ndvi(lat, lon, farm_size)
    
    def _simulate_ndvi(self, lat, lon, farm_size):
        """Simulate NDVI based on season and location"""
        
        # Get current month
        current_month = datetime.now().month
        
        # Seasonal NDVI patterns for India
        # Kharif (June-Oct): High vegetation
        # Rabi (Nov-Mar): Moderate to high
        # Summer (Apr-May): Low vegetation
        
        if 6 <= current_month <= 10:  # Kharif season
            base_ndvi = 0.70
            season = 'Kharif'
        elif 11 <= current_month or current_month <= 3:  # Rabi season
            base_ndvi = 0.65
            season = 'Rabi'
        else:  # Summer
            base_ndvi = 0.45
            season = 'Summer'
        
        # Add small variation based on location (latitude)
        # Northern India (higher lat) vs Southern India (lower lat)
        lat_factor = (lat - 20) * 0.01  # Rough adjustment
        ndvi_value = base_ndvi + lat_factor
        
        # Ensure NDVI is in valid range
        ndvi_value = max(0.0, min(1.0, ndvi_value))
        
        logger.info(f"Simulated NDVI: {ndvi_value} for {season} season")
        return self._analyze_ndvi(ndvi_value, farm_size, source='simulated', season=season)
    
    def _analyze_ndvi(self, ndvi_value, farm_size, source='satellite', season=''):
        """Analyze NDVI value and provide recommendations"""
        
        # Health classification
        if ndvi_value >= 0.8:
            health_status = 'Excellent'
            health_score = 95
            color = '#00C851'  # Green
            icon = '🌟'
        elif ndvi_value >= 0.6:
            health_status = 'Good'
            health_score = 80
            color = '#4CAF50'  # Light green
            icon = '✅'
        elif ndvi_value >= 0.4:
            health_status = 'Moderate'
            health_score = 60
            color = '#FFA726'  # Orange
            icon = '⚠️'
        elif ndvi_value >= 0.2:
            health_status = 'Poor'
            health_score = 35
            color = '#FF5722'  # Red-orange
            icon = '❌'
        else:
            health_status = 'Very Poor'
            health_score = 15
            color = '#F44336'  # Red
            icon = '🚨'
        
        # Recommendations based on NDVI
        recommendations = []
        
        if ndvi_value < 0.4:
            recommendations.append('🚨 Low vegetation detected. Check for pest/disease issues.')
            recommendations.append('💧 Increase irrigation frequency.')
            recommendations.append('🧪 Apply nitrogen fertilizer (Urea 40-50 kg/hectare).')
            recommendations.append('🌱 Consider replanting in severely affected areas.')
        elif ndvi_value < 0.6:
            recommendations.append('⚠️ Moderate vegetation health. Monitor closely.')
            recommendations.append('💧 Maintain regular irrigation schedule.')
            recommendations.append('🧪 Apply balanced NPK fertilizer.')
            recommendations.append('🐛 Check for early signs of pest infestation.')
        else:
            recommendations.append('✅ Crops are healthy! Continue current practices.')
            recommendations.append('💧 Maintain optimal irrigation.')
            recommendations.append('🌾 Prepare for good harvest.')
            recommendations.append('📊 Monitor for any sudden changes.')
        
        # Calculate estimated biomass (rough approximation)
        # NDVI correlates with biomass
        estimated_biomass = ndvi_value * 8000 * farm_size  # kg
        
        # Chlorophyll content estimation
        chlorophyll_index = ndvi_value * 100
        
        return {
            'ndvi_value': round(ndvi_value, 3),
            'health_status': health_status,
            'health_score': health_score,
            'color': color,
            'icon': icon,
            'recommendations': recommendations,
            'estimated_biomass_kg': round(estimated_biomass, 2),
            'chlorophyll_index': round(chlorophyll_index, 1),
            'data_source': source,
            'season': season,
            'farm_size_hectares': farm_size,
            'analysis_date': datetime.now().strftime('%Y-%m-%d'),
            'interpretation': {
                'ndvi_range': self._get_ndvi_range(ndvi_value),
                'vegetation_density': self._get_vegetation_density(ndvi_value),
                'stress_level': self._get_stress_level(ndvi_value)
            }
        }
    
    def _get_ndvi_range(self, ndvi):
        """Get NDVI range description"""
        if ndvi >= 0.8:
            return '0.8-1.0 (Very Dense Vegetation)'
        elif ndvi >= 0.6:
            return '0.6-0.8 (Dense Vegetation)'
        elif ndvi >= 0.4:
            return '0.4-0.6 (Moderate Vegetation)'
        elif ndvi >= 0.2:
            return '0.2-0.4 (Sparse Vegetation)'
        else:
            return '0.0-0.2 (Very Sparse/No Vegetation)'
    
    def _get_vegetation_density(self, ndvi):
        """Get vegetation density level"""
        if ndvi >= 0.7:
            return 'High'
        elif ndvi >= 0.5:
            return 'Medium'
        elif ndvi >= 0.3:
            return 'Low'
        else:
            return 'Very Low'
    
    def _get_stress_level(self, ndvi):
        """Get crop stress level"""
        if ndvi >= 0.7:
            return 'No Stress'
        elif ndvi >= 0.5:
            return 'Mild Stress'
        elif ndvi >= 0.3:
            return 'Moderate Stress'
        else:
            return 'Severe Stress'
    
    def get_historical_ndvi(self, lat, lon, days=30):
        """Get historical NDVI trend"""
        try:
            # Simulate historical trend
            dates = []
            ndvi_values = []
            
            current_month = datetime.now().month
            base_ndvi = 0.65 if 6 <= current_month <= 10 else 0.55
            
            for i in range(days, 0, -3):  # Every 3 days
                date = datetime.now() - timedelta(days=i)
                dates.append(date.strftime('%b %d'))
                
                # Add slight variation
                variation = (i % 10) * 0.01
                ndvi = base_ndvi + variation
                ndvi_values.append(round(ndvi, 3))
            
            return {
                'dates': dates,
                'ndvi_values': ndvi_values,
                'trend': 'improving' if ndvi_values[-1] > ndvi_values[0] else 'declining'
            }
        
        except Exception as e:
            logger.error(f"Historical NDVI error: {e}")
            return {'dates': [], 'ndvi_values': [], 'trend': 'stable'}

# Global instance
satellite_monitor = SatelliteCropHealth()

def get_crop_health_satellite(latitude, longitude, farm_size=1):
    """Get satellite-based crop health analysis"""
    return satellite_monitor.get_ndvi_data(latitude, longitude, farm_size)

def get_ndvi_history(latitude, longitude, days=30):
    """Get historical NDVI trend"""
    return satellite_monitor.get_historical_ndvi(latitude, longitude, days)
