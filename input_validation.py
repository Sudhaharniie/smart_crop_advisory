"""
Input Validation for Agricultural Data
Prevents unrealistic inputs and ensures data quality
"""

class InputValidator:
    """Validate all agricultural inputs"""
    
    # Valid ranges for agricultural parameters
    RANGES = {
        'nitrogen': {'min': 0, 'max': 140, 'unit': 'mg/kg', 'typical': (20, 80)},
        'phosphorus': {'min': 0, 'max': 145, 'unit': 'mg/kg', 'typical': (10, 50)},
        'potassium': {'min': 0, 'max': 205, 'unit': 'mg/kg', 'typical': (100, 300)},
        'ph': {'min': 0, 'max': 14, 'unit': '', 'typical': (5.5, 8.5)},
        'temperature': {'min': -10, 'max': 50, 'unit': '°C', 'typical': (15, 40)},
        'humidity': {'min': 0, 'max': 100, 'unit': '%', 'typical': (30, 90)},
        'rainfall': {'min': 0, 'max': 500, 'unit': 'mm', 'typical': (20, 300)},
        'moisture': {'min': 0, 'max': 100, 'unit': '%', 'typical': (40, 80)},
        'farm_size': {'min': 0.1, 'max': 10000, 'unit': 'hectares', 'typical': (0.5, 50)}
    }
    
    @staticmethod
    def validate_soil_params(nitrogen, phosphorus, potassium, ph):
        """Validate soil parameters"""
        errors = []
        warnings = []
        
        # Nitrogen validation
        if nitrogen < 0:
            errors.append("Nitrogen cannot be negative")
        elif nitrogen > InputValidator.RANGES['nitrogen']['max']:
            errors.append(f"Nitrogen too high (max: {InputValidator.RANGES['nitrogen']['max']} mg/kg)")
        elif nitrogen < InputValidator.RANGES['nitrogen']['typical'][0]:
            warnings.append(f"Nitrogen is low (typical: {InputValidator.RANGES['nitrogen']['typical'][0]}-{InputValidator.RANGES['nitrogen']['typical'][1]} mg/kg)")
        
        # Phosphorus validation
        if phosphorus < 0:
            errors.append("Phosphorus cannot be negative")
        elif phosphorus > InputValidator.RANGES['phosphorus']['max']:
            errors.append(f"Phosphorus too high (max: {InputValidator.RANGES['phosphorus']['max']} mg/kg)")
        elif phosphorus < InputValidator.RANGES['phosphorus']['typical'][0]:
            warnings.append(f"Phosphorus is low (typical: {InputValidator.RANGES['phosphorus']['typical'][0]}-{InputValidator.RANGES['phosphorus']['typical'][1]} mg/kg)")
        
        # Potassium validation
        if potassium < 0:
            errors.append("Potassium cannot be negative")
        elif potassium > InputValidator.RANGES['potassium']['max']:
            errors.append(f"Potassium too high (max: {InputValidator.RANGES['potassium']['max']} mg/kg)")
        elif potassium < InputValidator.RANGES['potassium']['typical'][0]:
            warnings.append(f"Potassium is low (typical: {InputValidator.RANGES['potassium']['typical'][0]}-{InputValidator.RANGES['potassium']['typical'][1]} mg/kg)")
        
        # pH validation
        if ph < InputValidator.RANGES['ph']['min'] or ph > InputValidator.RANGES['ph']['max']:
            errors.append(f"pH must be between {InputValidator.RANGES['ph']['min']} and {InputValidator.RANGES['ph']['max']}")
        elif ph < 5.5:
            warnings.append("Soil is acidic (pH < 5.5). Consider adding lime")
        elif ph > 8.5:
            warnings.append("Soil is alkaline (pH > 8.5). Consider adding gypsum")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }
    
    @staticmethod
    def validate_weather_params(temperature, humidity, rainfall):
        """Validate weather parameters"""
        errors = []
        warnings = []
        
        # Temperature validation
        if temperature < InputValidator.RANGES['temperature']['min']:
            errors.append(f"Temperature too low (min: {InputValidator.RANGES['temperature']['min']}°C)")
        elif temperature > InputValidator.RANGES['temperature']['max']:
            errors.append(f"Temperature too high (max: {InputValidator.RANGES['temperature']['max']}°C)")
        elif temperature > 40:
            warnings.append("High temperature detected. Crops may experience heat stress")
        elif temperature < 10:
            warnings.append("Low temperature detected. Risk of frost damage")
        
        # Humidity validation
        if humidity < 0 or humidity > 100:
            errors.append("Humidity must be between 0% and 100%")
        elif humidity < 30:
            warnings.append("Low humidity. Increase irrigation frequency")
        elif humidity > 90:
            warnings.append("High humidity. Risk of fungal diseases")
        
        # Rainfall validation
        if rainfall < 0:
            errors.append("Rainfall cannot be negative")
        elif rainfall > InputValidator.RANGES['rainfall']['max']:
            errors.append(f"Rainfall too high (max: {InputValidator.RANGES['rainfall']['max']} mm)")
        elif rainfall > 200:
            warnings.append("Heavy rainfall. Ensure proper drainage")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }
    
    @staticmethod
    def validate_farm_size(farm_size):
        """Validate farm size"""
        errors = []
        warnings = []
        
        if farm_size <= 0:
            errors.append("Farm size must be positive")
        elif farm_size > InputValidator.RANGES['farm_size']['max']:
            errors.append(f"Farm size too large (max: {InputValidator.RANGES['farm_size']['max']} hectares)")
        elif farm_size < 0.1:
            warnings.append("Very small farm size. Results may vary")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }
    
    @staticmethod
    def validate_all_inputs(nitrogen, phosphorus, potassium, ph, temperature, humidity, rainfall, farm_size=1):
        """Validate all inputs at once"""
        
        soil_validation = InputValidator.validate_soil_params(nitrogen, phosphorus, potassium, ph)
        weather_validation = InputValidator.validate_weather_params(temperature, humidity, rainfall)
        farm_validation = InputValidator.validate_farm_size(farm_size)
        
        all_errors = soil_validation['errors'] + weather_validation['errors'] + farm_validation['errors']
        all_warnings = soil_validation['warnings'] + weather_validation['warnings'] + farm_validation['warnings']
        
        return {
            'valid': len(all_errors) == 0,
            'errors': all_errors,
            'warnings': all_warnings,
            'details': {
                'soil': soil_validation,
                'weather': weather_validation,
                'farm': farm_validation
            }
        }
    
    @staticmethod
    def sanitize_input(value, param_name):
        """Sanitize and clamp input to valid range"""
        if param_name not in InputValidator.RANGES:
            return value
        
        range_info = InputValidator.RANGES[param_name]
        
        # Clamp to valid range
        value = max(range_info['min'], min(range_info['max'], value))
        
        return round(value, 2)

# Helper function for API routes
def validate_and_sanitize(data):
    """Validate and sanitize input data"""
    try:
        # Extract values
        nitrogen = float(data.get('nitrogen', 0))
        phosphorus = float(data.get('phosphorus', 0))
        potassium = float(data.get('potassium', 0))
        ph = float(data.get('ph', 7))
        temperature = float(data.get('temperature', 25))
        humidity = float(data.get('humidity', 60))
        rainfall = float(data.get('rainfall', 100))
        farm_size = float(data.get('farm_size', 1))
        
        # Validate
        validation = InputValidator.validate_all_inputs(
            nitrogen, phosphorus, potassium, ph,
            temperature, humidity, rainfall, farm_size
        )
        
        if not validation['valid']:
            return {
                'success': False,
                'errors': validation['errors'],
                'warnings': validation['warnings']
            }
        
        # Sanitize
        sanitized = {
            'nitrogen': InputValidator.sanitize_input(nitrogen, 'nitrogen'),
            'phosphorus': InputValidator.sanitize_input(phosphorus, 'phosphorus'),
            'potassium': InputValidator.sanitize_input(potassium, 'potassium'),
            'ph': InputValidator.sanitize_input(ph, 'ph'),
            'temperature': InputValidator.sanitize_input(temperature, 'temperature'),
            'humidity': InputValidator.sanitize_input(humidity, 'humidity'),
            'rainfall': InputValidator.sanitize_input(rainfall, 'rainfall'),
            'farm_size': InputValidator.sanitize_input(farm_size, 'farm_size')
        }
        
        return {
            'success': True,
            'data': sanitized,
            'warnings': validation['warnings']
        }
    
    except ValueError as e:
        return {
            'success': False,
            'errors': [f"Invalid input format: {str(e)}"],
            'warnings': []
        }
