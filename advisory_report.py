"""
Complete Smart Crop Advisory Report Generator
Combines all predictions into one comprehensive recommendation
"""

from datetime import datetime

class AdvisoryReportGenerator:
    """Generate complete farming advisory reports"""
    
    @staticmethod
    def generate_complete_advisory(user, soil_data, weather, top_3_crops, predicted_yield, 
                                   estimated_profit, irrigation_advice, fertilizer_recs, 
                                   market_prices, climate_risk=None):
        """
        Generate comprehensive farming advisory report
        
        Returns a complete decision-making report for farmers
        """
        
        best_crop = top_3_crops[0]
        
        report = {
            'header': {
                'title': 'Smart Crop Advisory Report',
                'farmer_name': user.username,
                'location': user.location,
                'farm_size': f"{user.farm_size} hectares",
                'report_date': datetime.now().strftime('%B %d, %Y'),
                'season': AdvisoryReportGenerator._get_current_season()
            },
            
            'crop_recommendation': {
                'primary_crop': {
                    'name': best_crop['crop'].title(),
                    'confidence': f"{best_crop['confidence']}%",
                    'suitability': 'Highly Suitable' if best_crop['confidence'] > 85 else 'Suitable',
                    'icon': '🌾'
                },
                'alternative_crops': [
                    {
                        'name': crop['crop'].title(),
                        'confidence': f"{crop['confidence']}%",
                        'rank': i + 2
                    }
                    for i, crop in enumerate(top_3_crops[1:])
                ],
                'recommendation_reason': AdvisoryReportGenerator._get_recommendation_reason(
                    best_crop['crop'], soil_data, weather
                )
            },
            
            'yield_and_profit': {
                'expected_yield': {
                    'value': f"{predicted_yield:,.0f} kg/hectare",
                    'total': f"{predicted_yield * user.farm_size:,.0f} kg",
                    'quality': 'High' if predicted_yield > 3500 else 'Medium'
                },
                'market_analysis': {
                    'current_price': f"₹{best_crop['price']}/quintal",
                    'trend': market_prices.get(best_crop['crop'].lower(), {}).get('trend', 'stable'),
                    'market_status': 'Favorable' if market_prices.get(best_crop['crop'].lower(), {}).get('trend') == 'up' else 'Stable'
                },
                'financial_projection': {
                    'gross_revenue': f"₹{best_crop['revenue']:,.0f}",
                    'estimated_costs': f"₹{best_crop['costs']:,.0f}",
                    'net_profit': f"₹{best_crop['profit']:,.0f}",
                    'roi': f"{best_crop['roi']}%",
                    'profit_per_hectare': f"₹{(best_crop['profit'] / user.farm_size):,.0f}",
                    'breakeven_yield': f"{(best_crop['costs'] / (best_crop['price'] / 100)):,.0f} kg"
                }
            },
            
            'weather_advisory': {
                'current_conditions': {
                    'temperature': f"{weather['temperature']}°C",
                    'humidity': f"{weather['humidity']}%",
                    'rainfall': f"{weather['rainfall']} mm",
                    'status': AdvisoryReportGenerator._get_weather_status(weather)
                },
                'farming_impact': AdvisoryReportGenerator._get_weather_impact(weather),
                'recommendations': irrigation_advice
            },
            
            'soil_health': {
                'status': AdvisoryReportGenerator._get_soil_health_status(soil_data),
                'parameters': {
                    'pH': {'value': soil_data['ph'], 'status': AdvisoryReportGenerator._get_ph_status(soil_data['ph'])},
                    'Nitrogen': {'value': f"{soil_data['nitrogen']} mg/kg", 'status': 'Good' if soil_data['nitrogen'] > 25 else 'Low'},
                    'Phosphorus': {'value': f"{soil_data['phosphorus']} mg/kg", 'status': 'Good' if soil_data['phosphorus'] > 15 else 'Low'},
                    'Potassium': {'value': f"{soil_data['potassium']} mg/kg", 'status': 'Good' if soil_data['potassium'] > 150 else 'Low'},
                    'Moisture': {'value': f"{soil_data['moisture']}%", 'status': 'Adequate' if soil_data['moisture'] > 50 else 'Low'}
                }
            },
            
            'fertilizer_plan': {
                'recommendations': fertilizer_recs,
                'application_schedule': AdvisoryReportGenerator._get_fertilizer_schedule(best_crop['crop']),
                'estimated_cost': AdvisoryReportGenerator._calculate_fertilizer_cost(fertilizer_recs, user.farm_size)
            },
            
            'irrigation_plan': {
                'method': 'Drip Irrigation (Recommended)' if user.farm_size > 2 else 'Sprinkler',
                'frequency': AdvisoryReportGenerator._get_irrigation_frequency(weather, soil_data),
                'water_requirement': f"{AdvisoryReportGenerator._calculate_water_requirement(best_crop['crop'], user.farm_size)} liters/day",
                'advice': irrigation_advice
            },
            
            'risk_assessment': {
                'climate_risk': climate_risk['overall_risk'] if climate_risk else 'Low',
                'pest_risk': 'Monitor regularly',
                'market_risk': 'Low' if best_crop['roi'] > 50 else 'Medium',
                'mitigation': AdvisoryReportGenerator._get_risk_mitigation(climate_risk)
            },
            
            'action_plan': {
                'immediate_actions': AdvisoryReportGenerator._get_immediate_actions(best_crop['crop'], soil_data, weather),
                'this_week': AdvisoryReportGenerator._get_weekly_tasks(best_crop['crop']),
                'this_month': AdvisoryReportGenerator._get_monthly_tasks(best_crop['crop'])
            },
            
            'summary': {
                'recommendation': f"Plant {best_crop['crop'].title()} for maximum profit",
                'confidence_level': 'High' if best_crop['confidence'] > 85 else 'Medium',
                'expected_outcome': f"Expected profit of ₹{best_crop['profit']:,.0f} with {best_crop['roi']}% ROI",
                'success_probability': f"{min(95, best_crop['confidence'] + 5)}%"
            }
        }
        
        return report
    
    @staticmethod
    def _get_current_season():
        month = datetime.now().month
        if 6 <= month <= 10:
            return 'Kharif (Monsoon)'
        elif 11 <= month or month <= 3:
            return 'Rabi (Winter)'
        else:
            return 'Zaid (Summer)'
    
    @staticmethod
    def _get_recommendation_reason(crop, soil_data, weather):
        reasons = []
        
        # Soil-based reasons
        if soil_data['nitrogen'] > 30:
            reasons.append(f"✅ High nitrogen level ({soil_data['nitrogen']} mg/kg) ideal for {crop}")
        if 6.0 <= soil_data['ph'] <= 7.5:
            reasons.append(f"✅ Optimal pH level ({soil_data['ph']}) for crop growth")
        
        # Weather-based reasons
        if 20 <= weather['temperature'] <= 35:
            reasons.append(f"✅ Suitable temperature ({weather['temperature']}°C) for {crop} cultivation")
        if weather['rainfall'] > 50:
            reasons.append(f"✅ Adequate rainfall ({weather['rainfall']} mm) for water requirements")
        
        # General
        reasons.append(f"✅ {crop.title()} has high market demand and good profit margins")
        
        return reasons
    
    @staticmethod
    def _get_weather_status(weather):
        if weather['temperature'] > 35:
            return 'Hot - Increase irrigation'
        elif weather['temperature'] < 15:
            return 'Cold - Monitor for frost'
        elif weather['rainfall'] > 100:
            return 'Heavy rain - Ensure drainage'
        else:
            return 'Favorable for farming'
    
    @staticmethod
    def _get_weather_impact(weather):
        if weather['temperature'] > 35:
            return 'High temperature may cause heat stress. Increase irrigation frequency.'
        elif weather['rainfall'] > 100:
            return 'Heavy rainfall expected. Ensure proper field drainage to prevent waterlogging.'
        else:
            return 'Weather conditions are favorable for farming activities.'
    
    @staticmethod
    def _get_soil_health_status(soil_data):
        score = 0
        if 6.0 <= soil_data['ph'] <= 7.5:
            score += 25
        if soil_data['nitrogen'] > 25:
            score += 25
        if soil_data['phosphorus'] > 15:
            score += 25
        if soil_data['potassium'] > 150:
            score += 25
        
        if score >= 75:
            return 'Excellent'
        elif score >= 50:
            return 'Good'
        else:
            return 'Needs Improvement'
    
    @staticmethod
    def _get_ph_status(ph):
        if ph < 5.5:
            return 'Acidic - Add lime'
        elif ph > 8.0:
            return 'Alkaline - Add gypsum'
        else:
            return 'Optimal'
    
    @staticmethod
    def _get_fertilizer_schedule(crop):
        return [
            {'stage': 'Base Application', 'timing': 'Before sowing', 'fertilizers': 'DAP + MOP'},
            {'stage': 'First Top Dressing', 'timing': '25-30 days after sowing', 'fertilizers': 'Urea'},
            {'stage': 'Second Top Dressing', 'timing': '45-50 days after sowing', 'fertilizers': 'Urea'}
        ]
    
    @staticmethod
    def _calculate_fertilizer_cost(fertilizer_recs, farm_size):
        # Rough estimate: ₹3000-5000 per hectare
        return f"₹{3500 * farm_size:,.0f} - ₹{5000 * farm_size:,.0f}"
    
    @staticmethod
    def _get_irrigation_frequency(weather, soil_data):
        if weather['rainfall'] > 50:
            return 'Reduce irrigation - adequate rainfall'
        elif soil_data['moisture'] < 50:
            return 'Every 3-4 days'
        else:
            return 'Every 5-7 days'
    
    @staticmethod
    def _calculate_water_requirement(crop, farm_size):
        # Rough estimate: 30-50 mm per week = 300-500 liters per hectare per day
        return int(400 * farm_size)
    
    @staticmethod
    def _get_risk_mitigation(climate_risk):
        if not climate_risk:
            return ['Monitor weather regularly', 'Maintain soil health']
        
        mitigation = []
        if climate_risk.get('drought', {}).get('level') in ['High', 'Critical']:
            mitigation.append('Install drip irrigation system')
        if climate_risk.get('flood', {}).get('level') in ['High', 'Critical']:
            mitigation.append('Ensure proper drainage channels')
        if climate_risk.get('heat_stress', {}).get('level') in ['High', 'Critical']:
            mitigation.append('Provide shade nets for sensitive crops')
        
        return mitigation if mitigation else ['No major risks detected']
    
    @staticmethod
    def _get_immediate_actions(crop, soil_data, weather):
        actions = []
        actions.append(f"🌱 Prepare land for {crop.title()} cultivation")
        
        if soil_data['ph'] < 6.0:
            actions.append("🧪 Apply lime to correct soil acidity")
        elif soil_data['ph'] > 8.0:
            actions.append("🧪 Apply gypsum to reduce alkalinity")
        
        if weather['rainfall'] < 20:
            actions.append("💧 Arrange irrigation water supply")
        
        actions.append("📦 Procure quality seeds from certified dealers")
        
        return actions
    
    @staticmethod
    def _get_weekly_tasks(crop):
        return [
            f"Sow {crop.title()} seeds with proper spacing",
            "Apply basal fertilizer (DAP + MOP)",
            "Ensure adequate moisture for germination",
            "Monitor for early pest infestation"
        ]
    
    @staticmethod
    def _get_monthly_tasks(crop):
        return [
            "First top dressing of Urea fertilizer",
            "Weed control - manual or herbicide",
            "Pest and disease monitoring",
            "Irrigation management based on weather"
        ]

# Helper function
def generate_advisory_report(user, soil_data, weather, top_3_crops, predicted_yield, 
                            estimated_profit, irrigation_advice, fertilizer_recs, 
                            market_prices, climate_risk=None):
    """Generate complete advisory report"""
    return AdvisoryReportGenerator.generate_complete_advisory(
        user, soil_data, weather, top_3_crops, predicted_yield,
        estimated_profit, irrigation_advice, fertilizer_recs,
        market_prices, climate_risk
    )
