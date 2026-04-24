"""
Comprehensive Crop Calendar
Month-wise farming activities for Indian agriculture
"""

CROP_CALENDAR = {
    'January': {
        'season': 'Rabi (Winter)',
        'temperature': '10-20°C',
        'activities': [
            '🌾 Rabi crops (Wheat, Chickpea, Mustard) are in vegetative stage',
            '💧 Irrigation: First irrigation 20-25 days after sowing',
            '🧪 Top dressing: Apply Urea (50 kg/hectare) for wheat',
            '🌱 Weed control: Manual weeding or herbicide application',
            '🐛 Pest watch: Monitor for aphids, termites',
            '📊 Soil preparation for summer crops begins',
            '🚜 Equipment maintenance for upcoming season'
        ],
        'crops_to_monitor': ['Wheat', 'Chickpea', 'Mustard', 'Barley', 'Lentil'],
        'harvesting': [],
        'sowing': ['Summer vegetables (protected cultivation)']
    },
    
    'February': {
        'season': 'Rabi (Late Winter)',
        'temperature': '15-25°C',
        'activities': [
            '🌾 Rabi crops entering flowering stage',
            '💧 Irrigation: Second irrigation for wheat (40-45 days)',
            '🧪 Foliar spray: Micronutrients (Zinc, Boron)',
            '🐛 Pest control: Spray for aphids if needed',
            '🌱 Weed management: Final weeding',
            '📊 Prepare for Zaid season crops',
            '🔍 Monitor crop maturity indicators'
        ],
        'crops_to_monitor': ['Wheat', 'Chickpea', 'Mustard', 'Potato'],
        'harvesting': ['Early potato', 'Cauliflower', 'Cabbage'],
        'sowing': ['Summer vegetables', 'Fodder crops']
    },
    
    'March': {
        'season': 'Zaid (Summer) begins',
        'temperature': '20-30°C',
        'activities': [
            '🌾 Rabi crop harvesting begins',
            '🚜 Harvest wheat when grain moisture is 20-25%',
            '🌱 Sow Zaid crops: Watermelon, Muskmelon, Cucumber',
            '💧 Increase irrigation frequency (every 5-7 days)',
            '📦 Dry and store harvested grains (12-14% moisture)',
            '🧪 Soil testing after Rabi harvest',
            '🌿 Prepare land for Kharif season'
        ],
        'crops_to_monitor': ['Wheat', 'Chickpea', 'Mustard'],
        'harvesting': ['Wheat', 'Chickpea', 'Mustard', 'Barley'],
        'sowing': ['Watermelon', 'Muskmelon', 'Cucumber', 'Vegetables']
    },
    
    'April': {
        'season': 'Zaid (Summer)',
        'temperature': '25-35°C',
        'activities': [
            '🌾 Complete Rabi harvest',
            '🌱 Zaid crops in growth stage',
            '💧 Frequent irrigation (every 3-5 days)',
            '🧪 Apply fertilizer to Zaid crops',
            '🐛 Monitor for fruit flies, aphids',
            '🌿 Deep ploughing for Kharif preparation',
            '📊 Plan Kharif crop selection'
        ],
        'crops_to_monitor': ['Watermelon', 'Muskmelon', 'Vegetables'],
        'harvesting': ['Late wheat', 'Lentil', 'Peas'],
        'sowing': ['Green manure crops', 'Fodder']
    },
    
    'May': {
        'season': 'Zaid (Late Summer)',
        'temperature': '30-40°C',
        'activities': [
            '🌾 Zaid crops nearing maturity',
            '💧 Critical irrigation period (every 2-3 days)',
            '🌿 Green manure incorporation',
            '🚜 Land preparation for Kharif (deep ploughing)',
            '🧪 Apply FYM/compost (5-10 tons/hectare)',
            '📦 Arrange seeds for Kharif crops',
            '🔧 Equipment check: Seed drill, sprayer'
        ],
        'crops_to_monitor': ['Watermelon', 'Muskmelon', 'Summer vegetables'],
        'harvesting': ['Watermelon', 'Muskmelon', 'Cucumber'],
        'sowing': ['Early Kharif (if monsoon arrives early)']
    },
    
    'June': {
        'season': 'Kharif (Monsoon) begins',
        'temperature': '28-35°C',
        'activities': [
            '🌧️ Monsoon arrival - Kharif sowing begins',
            '🌱 Sow: Rice, Cotton, Maize, Soybean, Groundnut',
            '💧 Utilize monsoon rain, supplementary irrigation if needed',
            '🧪 Basal fertilizer: DAP 50 kg + MOP 30 kg/hectare',
            '🌿 Weed control: Pre-emergence herbicide',
            '🐛 Seed treatment for pest/disease protection',
            '📊 Monitor rainfall and adjust sowing'
        ],
        'crops_to_monitor': ['Rice', 'Cotton', 'Maize', 'Soybean'],
        'harvesting': ['Late Zaid crops'],
        'sowing': ['Rice', 'Cotton', 'Maize', 'Soybean', 'Groundnut', 'Sugarcane']
    },
    
    'July': {
        'season': 'Kharif (Monsoon peak)',
        'temperature': '26-32°C',
        'activities': [
            '🌧️ Peak monsoon - complete Kharif sowing',
            '🌱 Transplant rice seedlings (20-25 days old)',
            '💧 Ensure proper drainage in fields',
            '🧪 First top dressing: Urea 40 kg/hectare (25-30 days)',
            '🌿 Weed management: Manual or herbicide',
            '🐛 Monitor for stem borer, leaf folder in rice',
            '📊 Gap filling in poorly germinated areas'
        ],
        'crops_to_monitor': ['Rice', 'Cotton', 'Maize', 'Soybean', 'Sugarcane'],
        'harvesting': [],
        'sowing': ['Late Kharif crops', 'Vegetables']
    },
    
    'August': {
        'season': 'Kharif (Monsoon)',
        'temperature': '25-30°C',
        'activities': [
            '🌾 Kharif crops in vegetative/flowering stage',
            '💧 Monitor water logging, ensure drainage',
            '🧪 Second top dressing: Urea 40 kg/hectare',
            '🐛 Pest control: Bollworm in cotton, stem borer in rice',
            '🌿 Weed control: Second weeding',
            '📊 Disease monitoring: Blight, wilt',
            '🌱 Prepare for Rabi season planning'
        ],
        'crops_to_monitor': ['Rice', 'Cotton', 'Maize', 'Soybean'],
        'harvesting': ['Early maize'],
        'sowing': []
    },
    
    'September': {
        'season': 'Kharif (Late Monsoon)',
        'temperature': '24-30°C',
        'activities': [
            '🌾 Kharif crops entering maturity',
            '💧 Reduce irrigation as monsoon recedes',
            '🧪 Stop nitrogen application',
            '🐛 Final pest control spray',
            '🌿 Prepare for harvesting',
            '📊 Rabi crop planning and seed arrangement',
            '🚜 Equipment preparation for harvest'
        ],
        'crops_to_monitor': ['Rice', 'Cotton', 'Soybean', 'Groundnut'],
        'harvesting': ['Maize', 'Early soybean'],
        'sowing': ['Early Rabi crops']
    },
    
    'October': {
        'season': 'Kharif harvest / Rabi sowing',
        'temperature': '20-28°C',
        'activities': [
            '🌾 Kharif harvest begins',
            '🚜 Harvest rice when 80% grains are golden',
            '🌱 Rabi sowing: Wheat, Chickpea, Mustard',
            '💧 Pre-sowing irrigation for Rabi crops',
            '🧪 Basal fertilizer: DAP 100 kg + MOP 50 kg/hectare',
            '📦 Dry and store Kharif harvest',
            '🌿 Crop residue management (compost, not burn)'
        ],
        'crops_to_monitor': ['Rice', 'Cotton', 'Soybean'],
        'harvesting': ['Rice', 'Soybean', 'Groundnut', 'Cotton (picking begins)'],
        'sowing': ['Wheat', 'Chickpea', 'Mustard', 'Barley', 'Lentil']
    },
    
    'November': {
        'season': 'Rabi (Winter) begins',
        'temperature': '15-25°C',
        'activities': [
            '🌾 Complete Kharif harvest',
            '🌱 Rabi crops in germination/early growth',
            '💧 Light irrigation if needed (10-15 days after sowing)',
            '🧪 Monitor crop establishment',
            '🌿 Weed control: Pre-emergence herbicide',
            '🐛 Protect from termites, cutworms',
            '📊 Cotton picking continues'
        ],
        'crops_to_monitor': ['Wheat', 'Chickpea', 'Mustard', 'Cotton'],
        'harvesting': ['Late rice', 'Cotton (continuous picking)'],
        'sowing': ['Late Rabi crops', 'Vegetables']
    },
    
    'December': {
        'season': 'Rabi (Winter)',
        'temperature': '10-20°C',
        'activities': [
            '🌾 Rabi crops in tillering/branching stage',
            '💧 First irrigation (20-25 days after sowing)',
            '🧪 First top dressing: Urea 50 kg/hectare',
            '🌿 Weed management: Manual weeding',
            '🐛 Monitor for aphids, caterpillars',
            '📊 Protect crops from frost (if applicable)',
            '🌱 Plan for next year crop rotation'
        ],
        'crops_to_monitor': ['Wheat', 'Chickpea', 'Mustard', 'Potato'],
        'harvesting': ['Cotton (final picking)', 'Sugarcane'],
        'sowing': ['Winter vegetables']
    }
}

def get_current_month_activities():
    """Get activities for current month"""
    current_month = datetime.now().strftime('%B')
    return CROP_CALENDAR.get(current_month, {})

def get_month_activities(month_name):
    """Get activities for specific month"""
    return CROP_CALENDAR.get(month_name, {})

def get_full_calendar():
    """Get complete crop calendar"""
    return CROP_CALENDAR

def get_seasonal_crops(season):
    """Get crops for specific season"""
    seasonal_crops = {
        'Kharif': ['Rice', 'Cotton', 'Maize', 'Soybean', 'Groundnut', 'Sugarcane', 'Bajra', 'Jowar'],
        'Rabi': ['Wheat', 'Chickpea', 'Mustard', 'Barley', 'Lentil', 'Peas', 'Potato', 'Onion'],
        'Zaid': ['Watermelon', 'Muskmelon', 'Cucumber', 'Vegetables', 'Fodder']
    }
    return seasonal_crops.get(season, [])
