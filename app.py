from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash, send_file
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import requests
import json
from datetime import datetime, timedelta
import sqlite3
import pandas as pd
import numpy as np
from gtts import gTTS
import os
import random
import joblib
from io import BytesIO
try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib import colors
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

model = joblib.load("model.pkl")
yield_model = joblib.load("yield_model.pkl")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crop_advisory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    farm_size = db.Column(db.Float, nullable=True)
    location = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(15), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class CropData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    crop_name = db.Column(db.String(50), nullable=False)
    planting_date = db.Column(db.Date, nullable=False)
    expected_harvest = db.Column(db.Date, nullable=True)
    current_stage = db.Column(db.String(50), nullable=True)
    area_planted = db.Column(db.Float, nullable=True)

class WeatherData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100), nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float, nullable=False)
    rainfall = db.Column(db.Float, nullable=False)
    wind_speed = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # income or expense
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

class Worker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15))
    daily_wage = db.Column(db.Float, nullable=False)
    task = db.Column(db.String(50))
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class SoilData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ph = db.Column(db.Float, default=6.8)
    nitrogen = db.Column(db.Float, default=25)
    phosphorus = db.Column(db.Float, default=18)
    potassium = db.Column(db.Float, default=180)
    moisture = db.Column(db.Float, default=65)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

class Equipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    icon = db.Column(db.String(50))
    rate = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20), default='day')
    distance = db.Column(db.Float)
    status = db.Column(db.String(20), default='Available')
    owner_contact = db.Column(db.String(15))

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String(200), nullable=False)
    icon = db.Column(db.String(50), default='bell')
    color = db.Column(db.String(20), default='info')
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    alert_type = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    sent_at = db.Column(db.DateTime, nullable=True)

class MarketplaceListing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    listing_type = db.Column(db.String(20), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500))
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Float)
    unit = db.Column(db.String(20))
    location = db.Column(db.String(100))
    contact = db.Column(db.String(15))
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    image_url = db.Column(db.String(200))

class DiseaseDetection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    crop_name = db.Column(db.String(50))
    disease_name = db.Column(db.String(100), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    severity = db.Column(db.String(20))
    treatment = db.Column(db.String(500))
    image_path = db.Column(db.String(200))
    detected_at = db.Column(db.DateTime, default=datetime.utcnow)
    resolved = db.Column(db.Boolean, default=False)

class LoanApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    loan_type = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    purpose = db.Column(db.String(200))
    status = db.Column(db.String(20), default='pending')
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
    approved_at = db.Column(db.DateTime, nullable=True)
    interest_rate = db.Column(db.Float)
    tenure_months = db.Column(db.Integer)

class Insurance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    scheme_name = db.Column(db.String(100), nullable=False)
    crop_covered = db.Column(db.String(50))
    sum_insured = db.Column(db.Float, nullable=False)
    premium = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='active')
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class VideoLibrary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500))
    category = db.Column(db.String(50))
    language = db.Column(db.String(10), default='en')
    duration = db.Column(db.Integer)
    video_url = db.Column(db.String(300), nullable=False)
    thumbnail_url = db.Column(db.String(300))
    views = db.Column(db.Integer, default=0)
    likes = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class VideoProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    video_id = db.Column(db.Integer, db.ForeignKey('video_library.id'), nullable=False)
    progress = db.Column(db.Float, default=0)
    completed = db.Column(db.Boolean, default=False)
    last_watched = db.Column(db.DateTime, default=datetime.utcnow)

# Weather API Integration
def get_weather_data(location):
    api_key ="0e83650f83704ae31b1719e1034b9d0d"

    # current weather
    current_url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
    current_res = requests.get(current_url).json()

    # rainfall logic
    rainfall = 0

    if "rain" in current_res:
        rainfall = current_res["rain"].get("1h", 0)

    if rainfall == 0:
        humidity = current_res["main"]["humidity"]
        clouds = current_res["clouds"]["all"]
        rainfall = round((humidity/100)*3 + (clouds/100)*2, 2)

    weather = {
        "temperature": current_res["main"]["temp"],
        "humidity": current_res["main"]["humidity"],
        "rainfall": rainfall,
        "wind_speed": current_res["wind"]["speed"],
        "description": current_res["weather"][0]["description"]
    }

    # 5 day / 3 hour forecast
    forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={location}&appid={api_key}&units=metric"
    forecast_res = requests.get(forecast_url).json()

    forecast = []

    for item in forecast_res["list"][:7]:
        forecast.append({
            "temp": item["main"]["temp"],
            "humidity": item["main"]["humidity"],
            "rain": item.get("rain", {}).get("3h", 0)
        })

    return weather, forecast

def generate_irrigation_advice(weather, forecast, soil_data):
    advice = []

    # rainfall logic (from forecast)
    total_rain = sum(day.get("rain", 0) for day in forecast)

    if total_rain > 10:
        advice.append("Rain expected this week. Reduce irrigation.")
    else:
        advice.append("Low rainfall forecast. Plan regular irrigation.")

    # temperature logic
    if weather["temperature"] and weather["temperature"] > 32:
        advice.append("High temperature detected. Increase irrigation frequency.")
    else:
        advice.append("Temperature normal. Standard irrigation is sufficient.")

    # soil moisture logic
    if soil_data["moisture"] < 50:
        advice.append("Soil moisture is low. Irrigation recommended today.")
    else:
        advice.append("Soil moisture level is adequate.")

    return advice

# Market Price API Integration
def get_market_prices():
    api_key = "579b464db66ec23bdd000001add664753a8345345eb493c8a6834fcd"

    url = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"
    
    params = {
        "api-key": api_key,
        "format": "json",
        "limit": 100
    }

    try:
        response = requests.get(url, params=params, timeout=5)
        data = response.json()

        prices = {}

        for item in data["records"]:
            crop = item.get("commodity", "").lower()
            price = float(item.get("modal_price", 0))

            if crop not in prices:
                prices[crop] = {
                    "current_price": price,
                    "last_week": price,
                    "trend": "stable"
                }
            else:
                last_price = prices[crop]["current_price"]

                trend = "stable"
                if price > last_price:
                    trend = "up"
                elif price < last_price:
                    trend = "down"

                prices[crop] = {
                    "current_price": price,
                    "last_week": last_price,
                    "trend": trend
                }

        return prices

    except Exception as e:
        print("Mandi API failed:", e)

        return {}

def get_user_soil_data(user_id):
    soil = SoilData.query.filter_by(user_id=user_id).first()
    if not soil:
        soil = SoilData(user_id=user_id)
        db.session.add(soil)
        db.session.commit()
    return {
        'ph': soil.ph,
        'nitrogen': soil.nitrogen,
        'phosphorus': soil.phosphorus,
        'potassium': soil.potassium,
        'moisture': soil.moisture
    }

# Soil Data Analysis
def analyze_soil_data(ph, nitrogen, phosphorus, potassium):
    """Analyze soil data and provide recommendations"""
    recommendations = []
    
    if ph < 5.5:
        recommendations.append("Soil is acidic. Add lime.")
    elif ph > 7.5:
        recommendations.append("Soil is alkaline. Add gypsum.")
    else:
        recommendations.append("Soil pH is optimal for most crops.")
    
    if nitrogen < 20:
        recommendations.append("Nitrogen is low.")
    else:
        recommendations.append("Nitrogen levels are adequate.")
    
    if phosphorus < 15:
        recommendations.append("Phosphorus is low.")
    else:
        recommendations.append("Phosphorus levels are good.")
    
    if potassium < 100:
        recommendations.append("Potassium is low.")
    else:
        recommendations.append("Potassium levels are adequate.")
    
    recommendations.append("Overall soil health is excellent!")
    
    return recommendations

# ML-based Crop Recommendation - TOP 3
def recommend_crops(N, P, K, temperature, humidity, ph, rainfall):
    import numpy as np
    features = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
    
    crop = model.predict(features)[0]
    prob = model.predict_proba(features)[0]
    
    # Get top 3 crops with probabilities
    top_3_indices = np.argsort(prob)[-3:][::-1]
    top_3_crops = []
    
    for idx in top_3_indices:
        crop_name = model.classes_[idx]
        confidence = round(prob[idx] * 100, 2)
        top_3_crops.append({
            'crop': crop_name,
            'confidence': confidence
        })
    
    return top_3_crops

def predict_yield(crop_name, weather):
    try:
        # encode crop same way as training
        crop_mapping = {
            "rice":0,"maize":1,"wheat":2,"cotton":3,"sugarcane":4
        }

        crop_code = crop_mapping.get(crop_name.lower(), 0)

        features = [[
            crop_code,
            weather["rainfall"],
            50000,   # avg fertilizer
            2000     # avg pesticide
        ]]

        y = yield_model.predict(features)[0]
        return round(float(y),2)

    except:
        return 0

# Routes
@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials')
    
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    farm_size = request.form.get('farm_size', 0)
    location = request.form.get('location', '')
    phone = request.form.get('phone', '')
    
    if User.query.filter_by(username=username).first():
        flash('Username already exists')
        return redirect(url_for('login'))
    
    new_user = User(
        username=username,
        email=email,
        password_hash=generate_password_hash(password),
        farm_size=float(farm_size) if farm_size else 0,
        location=location,
        phone=phone
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    session['user_id'] = new_user.id
    session['username'] = new_user.username
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    
    # Fetch all dashboard data
    weather, forecast = get_weather_data(user.location)

    market_prices = get_market_prices()
    if not market_prices:
        market_prices = {
            'rice': {'current_price': 2000, 'last_week': 1950, 'trend': 'up'},
            'wheat': {'current_price': 2500, 'last_week': 2500, 'trend': 'stable'},
            'maize': {'current_price': 1800, 'last_week': 1850, 'trend': 'down'},
            'cotton': {'current_price': 5500, 'last_week': 5400, 'trend': 'up'},
            'sugarcane': {'current_price': 3000, 'last_week': 3000, 'trend': 'stable'}
        }

    soil_data = get_user_soil_data(user.id)
    
    soil_recommendations = analyze_soil_data(
        soil_data['ph'], 
        soil_data['nitrogen'], 
        soil_data['phosphorus'], 
        soil_data['potassium']
    )
    
    # REAL ML crop recommendation - TOP 3
    top_3_crops = recommend_crops(
        soil_data['nitrogen'],
        soil_data['phosphorus'],
        soil_data['potassium'],
        weather['temperature'],
        weather['humidity'],
        soil_data['ph'],
        weather['rainfall']
    )
    
    # Calculate yield and profit for each crop with DIFFERENT prices
    crop_price_map = {
        'rice': 2000, 'wheat': 2500, 'maize': 1800, 'cotton': 5500, 
        'sugarcane': 3000, 'jute': 4200, 'coffee': 6000, 'chickpea': 5000,
        'kidneybeans': 8000, 'pigeonpeas': 6500, 'mothbeans': 5500,
        'mungbean': 7000, 'blackgram': 6800, 'lentil': 7500, 'pomegranate': 8000,
        'banana': 2000, 'mango': 4000, 'grapes': 6000, 'watermelon': 1500,
        'muskmelon': 2500, 'apple': 8000, 'papaya': 2000, 'coconut': 3500, 'orange': 4500
    }
    
    for crop_data in top_3_crops:
        crop_name = crop_data['crop']
        predicted_yield = predict_yield(crop_name, weather)
        
        # Get SPECIFIC market price for THIS crop
        crop_lower = crop_name.lower().strip()
        price = crop_price_map.get(crop_lower, 2500)  # Default 2500
        
        # Try to get from live market data
        for m in market_prices:
            if m.lower().strip() == crop_lower:
                price = market_prices[m]["current_price"]
                break
        
        # Calculate profit
        revenue = predicted_yield * price / 100  # Convert to quintal
        estimated_costs = (user.farm_size or 1) * 25000
        net_profit = revenue - estimated_costs
        
        crop_data['yield'] = predicted_yield
        crop_data['price'] = price
        crop_data['revenue'] = round(revenue, 2)
        crop_data['costs'] = round(estimated_costs, 2)
        crop_data['profit'] = round(net_profit, 2)
        crop_data['roi'] = round((net_profit / estimated_costs) * 100, 2) if estimated_costs > 0 else 0
    
    # Keep backward compatibility
    crop_recommendations = {
        "recommended_crop": top_3_crops[0]['crop'],
        "confidence": top_3_crops[0]['confidence'],
        "top_3": top_3_crops
    }
    
    predicted_yield = top_3_crops[0]['yield']
    estimated_profit = top_3_crops[0]['profit']

    # irrigation advice
    irrigation_advice = generate_irrigation_advice(weather, forecast, soil_data)

    # Dynamic Sustainability metrics
    total_expenses = Expense.query.filter_by(user_id=user.id).all()
    pesticide_expense = sum(e.amount for e in total_expenses if 'pesticide' in e.category.lower())
    fertilizer_expense = sum(e.amount for e in total_expenses if 'fertilizer' in e.category.lower())
    
    water_efficiency = min(95, 60 + (soil_data['moisture'] / 3))
    soil_health_score = min(100, (soil_data['nitrogen'] + soil_data['phosphorus'] + soil_data['potassium']/2) / 2)
    
    sustainability_data = {
        'water_usage_efficiency': round(water_efficiency, 1),
        'carbon_footprint': 'Low' if fertilizer_expense < 20000 else 'Medium',
        'pesticide_usage': 'Minimal' if pesticide_expense < 5000 else 'Moderate',
        'biodiversity_score': round(85 - (pesticide_expense / 500), 1),
        'eco_friendly_rating': round(4.5 - (pesticide_expense / 10000), 1),
        'soil_health': round(soil_health_score, 1),
        'organic_usage': 65,
        'water_saved': round(water_efficiency * 15, 0)
    }
    
    # Dynamic Irrigation schedule based on weather
    irrigation_schedule = []
    for i in range(3):
        future_date = datetime.now() + timedelta(days=i*3)
        amount = '20mm' if weather['rainfall'] > 5 else '30mm'
        irr_type = 'Drip irrigation' if soil_data['moisture'] < 60 else 'Sprinkler'
        irrigation_schedule.append({
            'date': future_date.strftime('%Y-%m-%d'),
            'amount': amount,
            'type': irr_type
        })
    
    # Dynamic Fertilizer recommendations based on soil
    fertilizer_recommendations = []
    if soil_data['nitrogen'] < 30:
        fertilizer_recommendations.append({'name': 'Urea', 'quantity': '40kg/hectare', 'timing': 'Immediate'})
    if soil_data['phosphorus'] < 20:
        fertilizer_recommendations.append({'name': 'DAP', 'quantity': '50kg/hectare', 'timing': 'Base application'})
    if soil_data['potassium'] < 150:
        fertilizer_recommendations.append({'name': 'MOP', 'quantity': '30kg/hectare', 'timing': 'Base application'})
    if not fertilizer_recommendations:
        fertilizer_recommendations.append({'name': 'Organic Compost', 'quantity': '500kg/hectare', 'timing': 'Maintenance'})
    
    # Government Schemes
    govt_schemes = [
        {'name': 'PM-KISAN', 'benefit': '₹6000/year direct transfer', 'eligibility': 'All landholding farmers'},
        {'name': 'Soil Health Card', 'benefit': 'Free soil testing', 'eligibility': 'All farmers'},
        {'name': 'Pradhan Mantri Fasal Bima Yojana', 'benefit': 'Crop insurance at 2% premium', 'eligibility': 'All farmers'},
        {'name': 'Kisan Credit Card', 'benefit': 'Low interest farm loans', 'eligibility': 'Farmers with land records'}
    ]
    
    # Crop Calendar
    crop_calendar = {
        'Kharif': {'season': 'June-October', 'crops': 'Rice, Cotton, Maize, Soybean'},
        'Rabi': {'season': 'October-March', 'crops': 'Wheat, Barley, Mustard, Chickpea'},
        'Zaid': {'season': 'March-June', 'crops': 'Watermelon, Cucumber, Vegetables'}
    }
    
    # Storage Tips
    storage_tips = [
        'Clean and dry grains before storage (12-14% moisture)',
        'Use airtight containers or hermetic bags',
        'Store in cool, dry place away from sunlight',
        'Check regularly for pests and moisture',
        'Use neem leaves as natural pest repellent'
    ]
    
    # Helpline
    helplines = [
        {'name': 'Kisan Call Centre', 'number': '1800-180-1551', 'service': '24x7 farming advice'},
        {'name': 'PM-KISAN Helpline', 'number': '155261 / 011-24300606', 'service': 'Scheme queries'},
        {'name': 'Soil Health Card', 'number': '011-24305948', 'service': 'Soil testing info'}
    ]
    
    # Dynamic Smart Notifications
    user_notifications = Notification.query.filter_by(user_id=user.id, is_read=False).order_by(Notification.created_at.desc()).limit(5).all()
    
    notifications = []
    for notif in user_notifications:
        notifications.append({
            'title': notif.title,
            'message': notif.message,
            'date': notif.created_at.strftime('%b %d'),
            'icon': notif.icon,
            'color': notif.color
        })
    
    # Auto-generate notifications if none exist
    if not notifications:
        if soil_data['moisture'] < 50:
            notifications.append({'title': 'Irrigation Alert', 'message': 'Soil moisture low. Water crops today', 'date': 'Today', 'icon': 'tint', 'color': 'warning'})
        if weather['temperature'] > 35:
            notifications.append({'title': 'Heat Alert', 'message': 'High temperature. Monitor crops closely', 'date': 'Today', 'icon': 'thermometer', 'color': 'danger'})
        notifications.append({'title': 'Weather Update', 'message': f"{weather['description'].capitalize()}", 'date': 'Today', 'icon': 'cloud', 'color': 'info'})
    
    # NEW FEATURES DATA
    # Marketplace listings from database
    marketplace_listings = MarketplaceListing.query.filter_by(status='active').order_by(MarketplaceListing.created_at.desc()).limit(8).all()
    marketplace_data = [{
        'id': l.id,
        'type': l.listing_type,
        'category': l.category,
        'title': l.title,
        'description': l.description,
        'price': l.price,
        'quantity': l.quantity,
        'unit': l.unit,
        'location': l.location,
        'contact': l.contact
    } for l in marketplace_listings]
    
    # Sample data if empty
    if not marketplace_data:
        marketplace_data = [
            {'title': 'Fresh Wheat', 'price': 2400, 'quantity': 100, 'unit': 'Quintal', 'type': 'sell', 'category': 'crop'},
            {'title': 'Tractor Rent', 'price': 1200, 'quantity': 1, 'unit': 'Day', 'type': 'rent', 'category': 'equipment'},
            {'title': 'Organic Seeds', 'price': 500, 'quantity': 1, 'unit': 'Kg', 'type': 'sell', 'category': 'seeds'},
            {'title': 'Need Workers', 'price': 500, 'quantity': 5, 'unit': 'Day', 'type': 'hire', 'category': 'labor'}
        ]
    
    # Disease detection history
    disease_history = DiseaseDetection.query.filter_by(user_id=user.id).order_by(DiseaseDetection.detected_at.desc()).limit(5).all()
    disease_data = [{
        'disease': d.disease_name,
        'confidence': d.confidence,
        'severity': d.severity,
        'treatment': d.treatment,
        'date': d.detected_at.strftime('%Y-%m-%d'),
        'resolved': d.resolved
    } for d in disease_history]
    
    # Loan eligibility
    total_income = sum(e.amount for e in Expense.query.filter_by(user_id=user.id, type='income').all())
    farm_size = user.farm_size or 1
    max_loan = farm_size * 50000
    loan_eligible = total_income > 50000
    loan_data = {
        'eligible': loan_eligible,
        'max_amount': min(max_loan, total_income * 2) if loan_eligible else 0,
        'interest_rate': 7.5
    }
    
    # Insurance plans
    insurance_plans = [
        {'name': 'PM Fasal Bima Yojana', 'premium_rate': 2.0, 'coverage': 'All natural calamities', 'max_coverage': 200000},
        {'name': 'Weather Based Crop Insurance', 'premium_rate': 3.5, 'coverage': 'Weather-related losses', 'max_coverage': 150000},
        {'name': 'Comprehensive Crop Insurance', 'premium_rate': 5.0, 'coverage': 'All risks including pests', 'max_coverage': 300000}
    ]
    
    # Video library
    videos = VideoLibrary.query.order_by(VideoLibrary.views.desc()).limit(6).all()
    video_data = [{
        'id': v.id,
        'title': v.title,
        'description': v.description,
        'category': v.category,
        'duration': v.duration,
        'views': v.views,
        'likes': v.likes
    } for v in videos]
    
    # Sample videos if empty
    if not video_data:
        video_data = [
            {'id': 1, 'title': 'Modern Drip Irrigation Techniques', 'duration': 180, 'views': 1200, 'category': 'technique', 'video_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'},
            {'id': 2, 'title': 'Organic Farming Success Stories', 'duration': 240, 'views': 980, 'category': 'success_story', 'video_url': 'https://www.youtube.com/watch?v=jNQXAC9IVRw'},
            {'id': 3, 'title': 'PM-KISAN Scheme Complete Guide', 'duration': 300, 'views': 2500, 'category': 'scheme', 'video_url': 'https://www.youtube.com/watch?v=9bZkp7q19f0'},
            {'id': 4, 'title': 'Soil Health Management', 'duration': 220, 'views': 1500, 'category': 'technique', 'video_url': 'https://www.youtube.com/watch?v=kJQP7kiw5Fk'},
            {'id': 5, 'title': 'Smart Farming with Technology', 'duration': 280, 'views': 1800, 'category': 'technique', 'video_url': 'https://www.youtube.com/watch?v=OPf0YbXqDm0'},
            {'id': 6, 'title': 'Crop Insurance Benefits', 'duration': 200, 'views': 900, 'category': 'scheme', 'video_url': 'https://www.youtube.com/watch?v=L_jWHffIx5E'}
        ]
    
    # SMS Alerts
    recent_alerts = Alert.query.filter_by(user_id=user.id).order_by(Alert.created_at.desc()).limit(5).all()
    alerts_data = [{
        'type': a.alert_type,
        'message': a.message,
        'status': a.status,
        'date': a.created_at.strftime('%b %d, %I:%M %p')
    } for a in recent_alerts]
    
    # Auto-generate sample alerts if empty
    if not alerts_data:
        alerts_data = [
            {'type': 'weather', 'message': 'Rain expected tomorrow', 'status': 'sent', 'date': 'Today 9:00 AM'},
            {'type': 'price', 'message': 'Wheat price increased to ₹2500', 'status': 'sent', 'date': 'Yesterday 6:00 PM'},
            {'type': 'irrigation', 'message': 'Time to water your crops', 'status': 'sent', 'date': '2 days ago'}
        ]
    
    # Expense Tracker - FETCH FROM DATABASE
    user_expenses = Expense.query.filter_by(user_id=user.id).order_by(Expense.date.desc()).limit(10).all()
    
    total_income = sum(e.amount for e in Expense.query.filter_by(user_id=user.id, type='income').all())
    total_expense = sum(e.amount for e in Expense.query.filter_by(user_id=user.id, type='expense').all())
    
    expenses = {
        'total_income': total_income if total_income else 0,
        'total_expense': total_expense if total_expense else 0,
        'net_profit': (total_income - total_expense) if (total_income and total_expense) else 0,
        'transactions': [{
            'type': e.type,
            'description': e.description,
            'amount': e.amount,
            'category': e.category
        } for e in user_expenses]
    }
    
    # If no transactions, show sample data
    if not user_expenses:
        expenses = {
            'total_income': 125000,
            'total_expense': 78000,
            'net_profit': 47000,
            'transactions': [
                {'type': 'income', 'description': 'Wheat Sale', 'amount': 50000, 'category': 'Crop Sale'},
                {'type': 'expense', 'description': 'Fertilizer Purchase', 'amount': 15000, 'category': 'Fertilizer'},
                {'type': 'expense', 'description': 'Labor Cost', 'amount': 20000, 'category': 'Labor'},
                {'type': 'income', 'description': 'Rice Sale', 'amount': 75000, 'category': 'Crop Sale'},
                {'type': 'expense', 'description': 'Seeds', 'amount': 8000, 'category': 'Seeds'}
            ]
        }
    
    # Dynamic Equipment Rental from database
    equipment_list = Equipment.query.all()
    equipment = []
    for eq in equipment_list:
        equipment.append({
            'name': eq.name,
            'icon': eq.icon,
            'rate': eq.rate,
            'unit': eq.unit,
            'distance': eq.distance,
            'status': eq.status
        })
    
    # Add default equipment if database is empty
    if not equipment:
        default_equipment = [
            {'name': 'Tractor', 'icon': 'tractor', 'rate': 800, 'unit': 'day', 'distance': 3, 'status': 'Available'},
            {'name': 'Harvester', 'icon': 'cog', 'rate': 1500, 'unit': 'day', 'distance': 5, 'status': 'Available'},
            {'name': 'Sprayer', 'icon': 'spray-can', 'rate': 300, 'unit': 'day', 'distance': 2, 'status': 'Available'}
        ]
        for eq_data in default_equipment:
            new_eq = Equipment(**eq_data)
            db.session.add(new_eq)
        db.session.commit()
        equipment = default_equipment
    
    # Dynamic Labor Management from database
    workers = Worker.query.filter_by(user_id=user.id, status='active').all()
    total_wages = sum(w.daily_wage for w in workers)
    
    labor = {
        'present': len(workers),
        'absent': 0,
        'total_wages': total_wages,
        'workers': [{
            'name': w.name,
            'wage': w.daily_wage,
            'task': w.task or 'General'
        } for w in workers]
    }
    
    # Sample data if no workers
    if not workers:
        labor = {
            'present': 0,
            'absent': 0,
            'total_wages': 0,
            'workers': []
        }
    
    dashboard_data = {
        'user': user,
        'weather': weather,
        'forecast': forecast,
        'market_prices': market_prices,
        'soil_data': soil_data,
        'soil_recommendations': soil_recommendations,
        'crop_recommendations': crop_recommendations,
        'irrigation_advice': irrigation_advice,
        'predicted_yield': predicted_yield,
        'estimated_profit': estimated_profit,
        'sustainability_data': sustainability_data,
        'irrigation_schedule': irrigation_schedule,
        'fertilizer_recommendations': fertilizer_recommendations,
        'govt_schemes': govt_schemes,
        'crop_calendar': crop_calendar,
        'storage_tips': storage_tips,
        'helplines': helplines,
        'notifications': notifications,
        'expenses': expenses,
        'equipment': equipment,
        'labor': labor,
        'marketplace_listings': marketplace_data,
        'disease_history': disease_data,
        'loan_data': loan_data,
        'insurance_plans': insurance_plans,
        'videos': video_data,
        'alerts': alerts_data
    }

    chart_data = {
        "soil": [
            soil_data['nitrogen'],
            soil_data['phosphorus'],
            soil_data['potassium']
        ],
        "profit": estimated_profit,
        "yield": predicted_yield,
        "weather": {
            "temperature": weather['temperature'],
            "humidity": weather['humidity'],
            "rainfall": weather['rainfall']
        },
        "forecast": [day['temp'] for day in forecast],
        "sustainability": {
            "soil_health": sustainability_data['soil_health'],
            "organic_usage": sustainability_data['organic_usage'],
            "biodiversity": sustainability_data['biodiversity_score'],
            "water_efficiency": sustainability_data['water_usage_efficiency']
        },
        "market_trends": list(market_prices.values())[:5] if market_prices else []
    }

    return render_template('dashboard.html', **dashboard_data, chart_data=chart_data)

@app.route('/api/voice_synthesis', methods=['POST'])
def voice_synthesis():
    """Generate voice for dashboard content"""
    data = request.get_json()
    text = data.get('text', '')
    language = data.get('language', 'en')
    
    # Language mapping for gTTS
    lang_map = {
        'en': 'en',
        'hi': 'hi',
        'bn': 'bn',
        'te': 'te',
        'ta': 'ta',
        'gu': 'gu',
        'mr': 'mr',
        'kn': 'kn'
    }
    
    try:
        tts = gTTS(text=text, lang=lang_map.get(language, 'en'))
        filename = f"voice_{datetime.now().timestamp()}.mp3"
        filepath = os.path.join('static', 'audio', filename)
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        tts.save(filepath)
        return jsonify({'audio_url': f'/static/audio/{filename}'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/crop_monitoring')
def crop_monitoring_api():
    """API endpoint for crop monitoring data"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    # Simulate crop growth data
    growth_data = {
        'growth_stage': 'Flowering',
        'days_since_planting': 45,
        'expected_harvest_days': 30,
        'plant_height': '65cm',
        'health_score': 8.5,
        'disease_risk': 'Low',
        'pest_alert': 'None',
        'yield_prediction': '2.5 tons/hectare'
    }
    
    return jsonify(growth_data)

@app.route('/api/sustainability_metrics')
def sustainability_metrics_api():
    """API endpoint for sustainability metrics"""
    metrics = {
        'water_conservation': {
            'current_usage': 450,  # liters per day
            'recommended': 400,
            'savings': 50,
            'efficiency': 89
        },
        'carbon_footprint': {
            'current': 1.2,  # tons CO2/hectare
            'target': 1.0,
            'reduction': 16.7
        },
        'biodiversity': {
            'beneficial_insects': 85,
            'soil_health': 78,
            'native_plants': 92
        },
        'chemical_usage': {
            'pesticides': 'Reduced by 40%',
            'fertilizers': 'Organic preferred',
            'herbicides': 'Minimal use'
        }
    }
    return jsonify(metrics)

@app.route('/api/pest_detection', methods=['POST'])
def pest_detection():
    """Detect pest/disease from uploaded image"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    
    # Simulate AI detection
    diseases = [
        {'name': 'Healthy', 'confidence': 95.5, 'severity': 'none', 
         'treatment': 'No treatment needed. Continue regular monitoring.'},
        {'name': 'Leaf Blight', 'confidence': 88.3, 'severity': 'medium',
         'treatment': 'Apply copper-based fungicide. Remove infected leaves.'},
        {'name': 'Aphid Infestation', 'confidence': 92.1, 'severity': 'low',
         'treatment': 'Use neem oil spray. Introduce ladybugs.'},
        {'name': 'Powdery Mildew', 'confidence': 85.7, 'severity': 'medium',
         'treatment': 'Apply sulfur-based fungicide. Improve air circulation.'},
        {'name': 'Rust', 'confidence': 90.2, 'severity': 'high',
         'treatment': 'Remove infected parts. Apply appropriate fungicide.'}
    ]
    detected = random.choice(diseases)
    
    # Save detection to database
    detection = DiseaseDetection(
        user_id=session['user_id'],
        disease_name=detected['name'],
        confidence=detected['confidence'],
        severity=detected['severity'],
        treatment=detected['treatment']
    )
    db.session.add(detection)
    db.session.commit()
    
    return jsonify({
        'disease': detected['name'],
        'confidence': detected['confidence'],
        'treatment': detected['treatment'],
        'severity': detected['severity']
    })

@app.route('/api/add_expense', methods=['POST'])
def add_expense():
    """Add income/expense transaction"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    
    new_expense = Expense(
        user_id=session['user_id'],
        type=data.get('type'),
        description=data.get('description'),
        amount=data.get('amount'),
        category=data.get('category')
    )
    
    db.session.add(new_expense)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Transaction added successfully'})

@app.route('/api/chatbot', methods=['POST'])
def chatbot():
    """AI Chatbot responses"""
    data = request.get_json()
    question = data.get('question', '').lower()
    
    responses = {
        'weather': 'Current weather is good for farming. Temperature is moderate with expected rainfall.',
        'pest': 'For pest control, use neem oil spray. It\'s organic and effective against most pests.',
        'fertilizer': 'Apply NPK fertilizer during base application. Use organic compost for better soil health.',
        'irrigation': 'Water crops early morning or evening. Use drip irrigation to save 30% water.',
        'crop': 'Based on your soil and weather, rice and wheat are recommended crops for this season.',
        'price': 'Current market prices are favorable. Rice is ₹2000/quintal, Wheat is ₹2500/quintal.',
        'default': 'I can help with weather, pests, fertilizers, irrigation, crops, and market prices. What would you like to know?'
    }
    
    for key in responses:
        if key in question:
            return jsonify({'response': responses[key]})
    
    return jsonify({'response': responses['default']})

@app.route('/api/update_soil', methods=['POST'])
def update_soil():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    soil = SoilData.query.filter_by(user_id=session['user_id']).first()
    
    if not soil:
        soil = SoilData(user_id=session['user_id'])
        db.session.add(soil)
    
    soil.ph = data.get('ph', soil.ph)
    soil.nitrogen = data.get('nitrogen', soil.nitrogen)
    soil.phosphorus = data.get('phosphorus', soil.phosphorus)
    soil.potassium = data.get('potassium', soil.potassium)
    soil.moisture = data.get('moisture', soil.moisture)
    soil.updated_at = datetime.utcnow()
    
    db.session.commit()
    return jsonify({'success': True, 'message': 'Soil data updated'})

@app.route('/api/add_worker', methods=['POST'])
def add_worker():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    worker = Worker(
        user_id=session['user_id'],
        name=data.get('name'),
        phone=data.get('phone'),
        daily_wage=data.get('daily_wage'),
        task=data.get('task')
    )
    db.session.add(worker)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Worker added'})

@app.route('/api/add_notification', methods=['POST'])
def add_notification():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    notif = Notification(
        user_id=session['user_id'],
        title=data.get('title'),
        message=data.get('message'),
        icon=data.get('icon', 'bell'),
        color=data.get('color', 'info')
    )
    db.session.add(notif)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Notification created'})

@app.route('/update_soil', methods=['POST'])
def update_soil_form():
    if 'user_id' not in session:
        flash('Please login first')
        return redirect(url_for('login'))
    
    soil = SoilData.query.filter_by(user_id=session['user_id']).first()
    if not soil:
        soil = SoilData(user_id=session['user_id'])
        db.session.add(soil)
    
    soil.nitrogen = float(request.form.get('nitrogen', soil.nitrogen))
    soil.phosphorus = float(request.form.get('phosphorus', soil.phosphorus))
    soil.potassium = float(request.form.get('potassium', soil.potassium))
    soil.ph = float(request.form.get('ph', soil.ph))
    soil.moisture = float(request.form.get('moisture', soil.moisture))
    soil.updated_at = datetime.utcnow()
    
    db.session.commit()
    flash('Soil data updated successfully!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/api/book_equipment', methods=['POST'])
def book_equipment():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    equipment_id = data.get('equipment_id')
    
    equipment = Equipment.query.get(equipment_id)
    if equipment and equipment.status == 'Available':
        equipment.status = 'Booked'
        db.session.commit()
        return jsonify({'success': True, 'message': f'{equipment.name} booked successfully!'})
    
    return jsonify({'error': 'Equipment not available'}), 400

@app.route('/add_worker_form', methods=['POST'])
def add_worker_form():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    name = request.form.get('name')
    wage = request.form.get('wage')
    task = request.form.get('task', 'General')
    
    worker = Worker(
        user_id=session['user_id'],
        name=name,
        daily_wage=float(wage),
        task=task
    )
    db.session.add(worker)
    db.session.commit()
    
    flash(f'Worker {name} added successfully!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/api/marketplace/listings', methods=['GET'])
def get_marketplace_listings():
    listings = MarketplaceListing.query.filter_by(status='active').order_by(MarketplaceListing.created_at.desc()).all()
    return jsonify([{
        'id': l.id,
        'type': l.listing_type,
        'category': l.category,
        'title': l.title,
        'description': l.description,
        'price': l.price,
        'quantity': l.quantity,
        'unit': l.unit,
        'location': l.location,
        'contact': l.contact
    } for l in listings])

@app.route('/api/marketplace/add', methods=['POST'])
def add_marketplace_listing():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    data = request.get_json()
    listing = MarketplaceListing(
        user_id=session['user_id'],
        listing_type=data['type'],
        category=data['category'],
        title=data['title'],
        description=data.get('description'),
        price=data['price'],
        quantity=data.get('quantity'),
        unit=data.get('unit'),
        location=data.get('location'),
        contact=data.get('contact')
    )
    db.session.add(listing)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Listing added'})

@app.route('/api/disease_history', methods=['GET'])
def get_disease_history():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    detections = DiseaseDetection.query.filter_by(user_id=session['user_id']).order_by(DiseaseDetection.detected_at.desc()).limit(10).all()
    return jsonify([{
        'disease': d.disease_name,
        'confidence': d.confidence,
        'severity': d.severity,
        'treatment': d.treatment,
        'date': d.detected_at.strftime('%Y-%m-%d'),
        'resolved': d.resolved
    } for d in detections])

@app.route('/api/loan/eligibility', methods=['GET'])
def check_loan_eligibility():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    user = User.query.get(session['user_id'])
    expenses = Expense.query.filter_by(user_id=user.id, type='income').all()
    total_income = sum(e.amount for e in expenses)
    farm_size = user.farm_size or 1
    max_loan = farm_size * 50000
    eligible = total_income > 50000
    max_amount = min(max_loan, total_income * 2) if eligible else 0
    return jsonify({
        'eligible': eligible,
        'max_amount': max_amount,
        'interest_rate': 7.5,
        'reason': 'Based on farm size and income history'
    })

@app.route('/api/loan/apply', methods=['POST'])
def apply_loan():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    data = request.get_json()
    loan = LoanApplication(
        user_id=session['user_id'],
        loan_type=data['loan_type'],
        amount=data['amount'],
        purpose=data.get('purpose'),
        interest_rate=7.5,
        tenure_months=data.get('tenure_months', 12)
    )
    db.session.add(loan)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Loan application submitted'})

@app.route('/api/insurance/plans', methods=['GET'])
def get_insurance_plans():
    plans = [
        {'name': 'PM Fasal Bima Yojana', 'premium_rate': 2.0, 'coverage': 'All natural calamities', 'max_coverage': 200000},
        {'name': 'Weather Based Crop Insurance', 'premium_rate': 3.5, 'coverage': 'Weather-related losses', 'max_coverage': 150000},
        {'name': 'Comprehensive Crop Insurance', 'premium_rate': 5.0, 'coverage': 'All risks including pests', 'max_coverage': 300000}
    ]
    return jsonify(plans)

@app.route('/api/insurance/apply', methods=['POST'])
def apply_insurance():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    data = request.get_json()
    insurance = Insurance(
        user_id=session['user_id'],
        scheme_name=data['scheme_name'],
        crop_covered=data.get('crop_covered'),
        sum_insured=data['sum_insured'],
        premium=data['premium'],
        start_date=datetime.strptime(data['start_date'], '%Y-%m-%d').date(),
        end_date=datetime.strptime(data['end_date'], '%Y-%m-%d').date()
    )
    db.session.add(insurance)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Insurance application submitted'})

@app.route('/api/videos', methods=['GET'])
def get_videos():
    category = request.args.get('category')
    language = request.args.get('language', 'en')
    query = VideoLibrary.query
    if category:
        query = query.filter_by(category=category)
    if language:
        query = query.filter_by(language=language)
    videos = query.order_by(VideoLibrary.views.desc()).limit(20).all()
    return jsonify([{
        'id': v.id,
        'title': v.title,
        'description': v.description,
        'category': v.category,
        'duration': v.duration,
        'video_url': v.video_url,
        'thumbnail_url': v.thumbnail_url,
        'views': v.views,
        'likes': v.likes
    } for v in videos])

@app.route('/api/alerts/send', methods=['POST'])
def send_alert():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    data = request.get_json()
    user = User.query.get(session['user_id'])
    alert = Alert(
        user_id=user.id,
        alert_type=data['alert_type'],
        message=data['message'],
        phone=user.phone or data.get('phone')
    )
    db.session.add(alert)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Alert scheduled'})




# Multi-page routes
@app.route('/crops')
def crops():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    return render_template('crops.html', user=user)

@app.route('/weather')
def weather():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    weather, forecast = get_weather_data(user.location)
    return render_template('weather.html', user=user, weather=weather, forecast=forecast)

@app.route('/market')
def market():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    market_prices = get_market_prices() or {
        'rice': {'current_price': 2000, 'last_week': 1950, 'trend': 'up'},
        'wheat': {'current_price': 2500, 'last_week': 2500, 'trend': 'stable'},
        'maize': {'current_price': 1800, 'last_week': 1850, 'trend': 'down'},
        'cotton': {'current_price': 5500, 'last_week': 5400, 'trend': 'up'},
        'sugarcane': {'current_price': 3000, 'last_week': 3000, 'trend': 'stable'}
    }
    return render_template('market.html', user=user, market_prices=market_prices)

@app.route('/soil')
def soil():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    soil_data = get_user_soil_data(user.id)
    recommendations = analyze_soil_data(soil_data['ph'], soil_data['nitrogen'], soil_data['phosphorus'], soil_data['potassium'])
    return render_template('soil.html', user=user, soil_data=soil_data, recommendations=recommendations)

@app.route('/finance')
def finance():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    expenses = Expense.query.filter_by(user_id=user.id).order_by(Expense.date.desc()).all()
    total_income = sum(e.amount for e in Expense.query.filter_by(user_id=user.id, type='income').all())
    total_expense = sum(e.amount for e in Expense.query.filter_by(user_id=user.id, type='expense').all())
    return render_template('finance.html', user=user, expenses=expenses, total_income=total_income, total_expense=total_expense)

@app.route('/labor')
def labor():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    workers = Worker.query.filter_by(user_id=user.id, status='active').all()
    return render_template('labor.html', user=user, workers=workers)

@app.route('/equipment')
def equipment():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    equipment_list = Equipment.query.all()
    return render_template('equipment.html', user=user, equipment=equipment_list)

@app.route('/generate_report')
def generate_report():
    """Generate PDF report of dashboard data"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if not PDF_AVAILABLE:
        flash('PDF generation not available. Install reportlab: pip install reportlab', 'error')
        return redirect(url_for('dashboard'))
    
    user = User.query.get(session['user_id'])
    weather, forecast = get_weather_data(user.location)
    soil_data = get_user_soil_data(user.id)
    
    # Get crop recommendations
    top_3_crops = recommend_crops(
        soil_data['nitrogen'], soil_data['phosphorus'], soil_data['potassium'],
        weather['temperature'], weather['humidity'], soil_data['ph'], weather['rainfall']
    )
    
    # Create PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=50, leftMargin=50, topMargin=50, bottomMargin=50)
    elements = []
    styles = getSampleStyleSheet()
    
    # Title
    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=24, textColor=colors.HexColor('#2d5016'), spaceAfter=30, alignment=TA_CENTER)
    elements.append(Paragraph('Smart Crop Advisory Report', title_style))
    elements.append(Spacer(1, 12))
    
    # Farm Info
    info_style = ParagraphStyle('Info', parent=styles['Normal'], fontSize=12, spaceAfter=6)
    elements.append(Paragraph(f'<b>Farmer:</b> {user.username}', info_style))
    elements.append(Paragraph(f'<b>Farm Size:</b> {user.farm_size} hectares', info_style))
    elements.append(Paragraph(f'<b>Location:</b> {user.location}', info_style))
    elements.append(Paragraph(f'<b>Report Date:</b> {datetime.now().strftime("%B %d, %Y")}', info_style))
    elements.append(Spacer(1, 20))
    
    # Weather Section
    elements.append(Paragraph('<b>Current Weather Conditions</b>', styles['Heading2']))
    weather_data = [
        ['Parameter', 'Value'],
        ['Temperature', f"{weather['temperature']}°C"],
        ['Humidity', f"{weather['humidity']}%"],
        ['Rainfall', f"{weather['rainfall']}mm"],
        ['Wind Speed', f"{weather['wind_speed']} m/s"]
    ]
    weather_table = Table(weather_data, colWidths=[3*inch, 3*inch])
    weather_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4a7c2c')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(weather_table)
    elements.append(Spacer(1, 20))
    
    # Soil Health Section
    elements.append(Paragraph('<b>Soil Health Analysis</b>', styles['Heading2']))
    soil_table_data = [
        ['Parameter', 'Value', 'Status'],
        ['pH Level', f"{soil_data['ph']}", 'Optimal' if 5.5 <= soil_data['ph'] <= 7.5 else 'Needs Adjustment'],
        ['Nitrogen (N)', f"{soil_data['nitrogen']} mg/kg", 'Good' if soil_data['nitrogen'] >= 20 else 'Low'],
        ['Phosphorus (P)', f"{soil_data['phosphorus']} mg/kg", 'Good' if soil_data['phosphorus'] >= 15 else 'Low'],
        ['Potassium (K)', f"{soil_data['potassium']} mg/kg", 'Good' if soil_data['potassium'] >= 100 else 'Low'],
        ['Moisture', f"{soil_data['moisture']}%", 'Adequate' if soil_data['moisture'] >= 50 else 'Low']
    ]
    soil_table = Table(soil_table_data, colWidths=[2*inch, 2*inch, 2*inch])
    soil_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4a7c2c')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgreen),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(soil_table)
    elements.append(Spacer(1, 20))
    
    # Top 3 Crop Recommendations
    elements.append(Paragraph('<b>Top 3 Crop Recommendations</b>', styles['Heading2']))
    crop_data = [['Rank', 'Crop', 'Confidence', 'Est. Yield', 'Est. Profit', 'ROI']]
    for i, crop in enumerate(top_3_crops, 1):
        crop_data.append([
            f"#{i}",
            crop['crop'].title(),
            f"{crop['confidence']}%",
            f"{crop['yield']} kg/ha",
            f"₹{crop['profit']:,.0f}",
            f"{crop['roi']}%"
        ])
    crop_table = Table(crop_data, colWidths=[0.7*inch, 1.5*inch, 1.2*inch, 1.3*inch, 1.3*inch, 1*inch])
    crop_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2d5016')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (0, 1), colors.HexColor('#FFD700')),
        ('BACKGROUND', (0, 2), (0, 2), colors.HexColor('#C0C0C0')),
        ('BACKGROUND', (0, 3), (0, 3), colors.HexColor('#CD7F32')),
        ('BACKGROUND', (1, 1), (-1, -1), colors.lightgoldenrodyellow),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(crop_table)
    elements.append(Spacer(1, 15))
    
    # Profit Analysis for Best Crop
    best_crop = top_3_crops[0]
    elements.append(Paragraph(f'<b>Detailed Profit Analysis - {best_crop["crop"].title()}</b>', styles['Heading3']))
    profit_data = [
        ['Item', 'Amount'],
        ['Expected Yield', f"{best_crop['yield']} kg/hectare"],
        ['Market Price', f"₹{best_crop['price']}/quintal"],
        ['Gross Revenue', f"₹{best_crop['revenue']:,.2f}"],
        ['Estimated Costs', f"₹{best_crop['costs']:,.2f}"],
        ['Net Profit', f"₹{best_crop['profit']:,.2f}"],
        ['Return on Investment', f"{best_crop['roi']}%"]
    ]
    profit_table = Table(profit_data, colWidths=[3*inch, 3*inch])
    profit_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#6b9e3e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightcyan),
        ('BACKGROUND', (0, -2), (-1, -1), colors.HexColor('#90EE90')),
        ('FONTNAME', (0, -2), (-1, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(profit_table)
    elements.append(Spacer(1, 20))
    
    # Financial Summary
    expenses = Expense.query.filter_by(user_id=user.id).all()
    total_income = sum(e.amount for e in expenses if e.type == 'income')
    total_expense = sum(e.amount for e in expenses if e.type == 'expense')
    elements.append(Paragraph('<b>Financial Summary</b>', styles['Heading2']))
    finance_data = [
        ['Category', 'Amount'],
        ['Total Income', f"₹{total_income:,.2f}"],
        ['Total Expenses', f"₹{total_expense:,.2f}"],
        ['Net Profit/Loss', f"₹{(total_income - total_expense):,.2f}"]
    ]
    finance_table = Table(finance_data, colWidths=[3*inch, 3*inch])
    finance_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4a7c2c')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightyellow),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(finance_table)
    elements.append(Spacer(1, 20))
    
    # Footer
    footer_style = ParagraphStyle('Footer', parent=styles['Normal'], fontSize=9, textColor=colors.grey, alignment=TA_CENTER)
    elements.append(Spacer(1, 30))
    elements.append(Paragraph('Generated by Smart Crop Advisory System', footer_style))
    elements.append(Paragraph(f'Report ID: {user.id}-{datetime.now().strftime("%Y%m%d%H%M%S")}', footer_style))
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    
    return send_file(
        buffer,
        as_attachment=True,
        download_name=f'farm_report_{user.username}_{datetime.now().strftime("%Y%m%d")}.pdf',
        mimetype='application/pdf'
    )

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Initialize database
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
