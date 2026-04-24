# COMPLETE REAL & DYNAMIC PROJECT SETUP GUIDE

## 🎯 OBJECTIVE
Transform ALL static/rule-based features into real, dynamic, API-driven functionality

---

## 📋 STEP-BY-STEP IMPLEMENTATION

### PHASE 1: API KEYS & ACCOUNTS (Day 1)

#### 1. Weather Data (OpenWeatherMap)
```bash
# Sign up: https://openweathermap.org/api
# Free tier: 1,000 calls/day
# Get API key from dashboard
```
**Add to .env:**
```
OPENWEATHER_API_KEY=your_key_here
```

#### 2. Market Prices (Data.gov.in)
```bash
# Sign up: https://data.gov.in/
# Register for API access
# Get API key for Agmarknet data
```
**Add to .env:**
```
DATA_GOV_IN_KEY=your_key_here
```

#### 3. Disease Detection (Plant.id)
```bash
# Sign up: https://web.plant.id/
# Free tier: 100 identifications/month
# Paid: $29/month for 500 calls
```
**Add to .env:**
```
PLANTID_API_KEY=your_key_here
```

#### 4. SMS Alerts (Twilio)
```bash
# Sign up: https://www.twilio.com/
# Free trial: $15 credit
# Get Account SID, Auth Token, Phone Number
```
**Add to .env:**
```
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_PHONE_NUMBER=+1234567890
```

---

### PHASE 2: INSTALL DEPENDENCIES (Day 1)

```bash
pip install requests
pip install pandas numpy
pip install scikit-learn
pip install tensorflow  # For deep learning models
pip install opencv-python  # For image processing
pip install pillow
pip install geopy  # For location services
pip install twilio  # For SMS
pip install python-dotenv  # For environment variables
```

**Update requirements.txt:**
```txt
Flask==2.3.0
Flask-SQLAlchemy==3.0.0
requests==2.31.0
pandas==2.0.0
numpy==1.24.0
scikit-learn==1.3.0
tensorflow==2.13.0
opencv-python==4.8.0
Pillow==10.0.0
geopy==2.3.0
twilio==8.5.0
python-dotenv==1.0.0
joblib==1.3.0
reportlab==4.0.0
gtts==2.3.0
```

---

### PHASE 3: TRAIN REAL ML MODELS (Day 2-3)

#### 1. Download Real Datasets

**Crop Recommendation Dataset:**
```python
# Download from Kaggle
# https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset

import pandas as pd

# Load real data
df = pd.read_csv('Crop_recommendation.csv')
print(df.head())
print(f"Dataset size: {len(df)} samples")
```

**Crop Production Dataset (Government):**
```python
# Download from data.gov.in
url = "https://api.data.gov.in/resource/crop-production-statistics"
# Use this for yield prediction
```

**Plant Disease Dataset:**
```python
# PlantVillage Dataset (54,000+ images)
# https://github.com/spMohanty/PlantVillage-Dataset
# Download and extract
```

#### 2. Train Crop Recommendation Model

Create `train_real_crop_model.py`:
```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load REAL dataset
df = pd.read_csv('data/Crop_recommendation.csv')

X = df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
y = df['label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=200, random_state=42, max_depth=20)
model.fit(X_train, y_train)

# Evaluate
accuracy = model.score(X_test, y_test)
print(f"Model Accuracy: {accuracy * 100:.2f}%")

# Save model
joblib.dump(model, 'models/crop_recommendation_real.pkl')
print("Real model saved!")
```

Run:
```bash
python train_real_crop_model.py
```

#### 3. Train Disease Detection Model

Create `train_real_disease_model.py`:
```python
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Load PlantVillage dataset
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True,
    validation_split=0.2
)

train_generator = train_datagen.flow_from_directory(
    'data/PlantVillage/',
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical',
    subset='training'
)

validation_generator = train_datagen.flow_from_directory(
    'data/PlantVillage/',
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical',
    subset='validation'
)

# Build model
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(128, activation='relu')(x)
predictions = Dense(train_generator.num_classes, activation='softmax')(x)

model = Model(inputs=base_model.input, outputs=predictions)

# Freeze base model layers
for layer in base_model.layers:
    layer.trainable = False

# Compile
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train
history = model.fit(
    train_generator,
    epochs=10,
    validation_data=validation_generator
)

# Save
model.save('models/disease_detection_real.h5')
print("Real disease model saved!")
```

Run:
```bash
python train_real_disease_model.py
```

---

### PHASE 4: INTEGRATE REAL DATA SERVICES (Day 4-5)

#### 1. Update app.py

Replace the imports and functions in your `app.py` with the code from `app_real_integration.py`:

```python
# Copy the functions from app_real_integration.py into your app.py
# Replace:
# - get_weather_data()
# - get_market_prices()
# - recommend_crops()
# - predict_yield()
# - pest_detection route
```

#### 2. Create .env file

Create `.env` in project root:
```env
# Flask
SECRET_KEY=your-super-secret-key-change-this
DATABASE_URL=sqlite:///crop_advisory.db

# Weather API
OPENWEATHER_API_KEY=your_openweather_key

# Market Data
DATA_GOV_IN_KEY=your_data_gov_key
AGMARKNET_API_KEY=your_agmarknet_key

# Disease Detection
PLANTID_API_KEY=your_plantid_key

# SMS Service
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
TWILIO_PHONE_NUMBER=+1234567890

# IoT Sensors (if you have them)
IOT_SENSOR_ENDPOINT=http://your-sensor-ip:port

# NASA POWER API (Free, no key needed)
# Used for satellite agricultural data
```

#### 3. Load environment variables

Add to top of `app.py`:
```python
from dotenv import load_dotenv
load_dotenv()  # Load .env file
```

---

### PHASE 5: IOT SENSOR INTEGRATION (Optional - Day 6-7)

#### Hardware Setup (if you want real soil sensors)

**Components needed:**
- ESP32/Arduino board (~₹500)
- NPK Sensor (~₹3000)
- pH Sensor (~₹500)
- Moisture Sensor (~₹200)
- Jumper wires (~₹100)

**Arduino Code:**
```cpp
#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "your_wifi";
const char* password = "your_password";
const char* serverUrl = "http://your-server/api/soil/update";

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
}

void loop() {
  // Read sensors
  float nitrogen = readNPK_N();
  float phosphorus = readNPK_P();
  float potassium = readNPK_K();
  float ph = readPH();
  float moisture = readMoisture();
  
  // Send to server
  HTTPClient http;
  http.begin(serverUrl);
  http.addHeader("Content-Type", "application/json");
  
  String jsonData = "{\"N\":" + String(nitrogen) + 
                    ",\"P\":" + String(phosphorus) + 
                    ",\"K\":" + String(potassium) + 
                    ",\"pH\":" + String(ph) + 
                    ",\"moisture\":" + String(moisture) + "}";
  
  int httpCode = http.POST(jsonData);
  http.end();
  
  delay(300000); // Send every 5 minutes
}
```

---

### PHASE 6: DATABASE MIGRATION (Day 8)

#### Add new fields for real data tracking

Create `migrations.py`:
```python
from app import app, db, User

with app.app_context():
    # Add new columns
    db.engine.execute('ALTER TABLE user ADD COLUMN latitude REAL')
    db.engine.execute('ALTER TABLE user ADD COLUMN longitude REAL')
    db.engine.execute('ALTER TABLE user ADD COLUMN sensor_id VARCHAR(50)')
    
    db.engine.execute('ALTER TABLE soil_data ADD COLUMN sensor_reading BOOLEAN DEFAULT 0')
    db.engine.execute('ALTER TABLE soil_data ADD COLUMN conductivity REAL')
    db.engine.execute('ALTER TABLE soil_data ADD COLUMN temperature REAL')
    
    print("Database migrated successfully!")
```

Run:
```bash
python migrations.py
```

---

### PHASE 7: TESTING REAL DATA (Day 9)

#### Test Weather API
```python
from real_data_integration import weather_service

weather = weather_service.get_current_weather('Delhi')
print(weather)

forecast = weather_service.get_forecast('Mumbai', days=7)
print(forecast)
```

#### Test Market Prices
```python
from real_data_integration import market_service

prices = market_service.get_real_prices()
print(f"Found {len(prices)} crop prices")
for crop, data in list(prices.items())[:5]:
    print(f"{crop}: ₹{data['current_price']}")
```

#### Test Disease Detection
```python
from real_data_integration import disease_service

result = disease_service.detect_disease('test_image.jpg')
print(result)
```

#### Test Crop Recommendation
```python
from real_data_integration import crop_service

soil = {'nitrogen': 40, 'phosphorus': 30, 'potassium': 200, 'ph': 6.5, 'moisture': 60}
weather = {'temperature': 25, 'humidity': 70, 'rainfall': 100}

recommendations = crop_service.predict(soil, weather)
print(recommendations)
```

---

### PHASE 8: DEPLOYMENT (Day 10)

#### 1. Update requirements.txt
```bash
pip freeze > requirements.txt
```

#### 2. Set environment variables on server
```bash
export OPENWEATHER_API_KEY=your_key
export DATA_GOV_IN_KEY=your_key
export PLANTID_API_KEY=your_key
# etc...
```

#### 3. Run application
```bash
python app.py
```

---

## 🔍 VERIFICATION CHECKLIST

### ✅ Weather Data
- [ ] Real-time temperature from API
- [ ] Real humidity readings
- [ ] Actual rainfall data
- [ ] 7-day forecast working
- [ ] Weather alerts triggering

### ✅ Market Prices
- [ ] Prices from government API
- [ ] Daily price updates
- [ ] Real trend calculations (up/down/stable)
- [ ] Multiple crop prices available

### ✅ Crop Recommendation
- [ ] ML model trained on real data
- [ ] Accuracy > 85%
- [ ] Top 3 predictions working
- [ ] Confidence scores realistic

### ✅ Yield Prediction
- [ ] Using real historical data
- [ ] Weather-adjusted predictions
- [ ] Soil-based calculations
- [ ] Satellite data integration (optional)

### ✅ Disease Detection
- [ ] Real AI model (Plant.id or trained CNN)
- [ ] Confidence > 75%
- [ ] Treatment recommendations accurate
- [ ] Image upload working

### ✅ Irrigation Scheduling
- [ ] FAO-56 method implemented
- [ ] Real ET0 calculations
- [ ] Crop coefficient based
- [ ] Weather-adjusted

### ✅ Soil Data
- [ ] IoT sensor integration (if available)
- [ ] Manual input validation
- [ ] Real-time updates
- [ ] Historical tracking

### ✅ Financial Tracking
- [ ] Real transaction records
- [ ] Accurate calculations
- [ ] Category-wise breakdown
- [ ] Export functionality

### ✅ SMS Alerts
- [ ] Twilio integration working
- [ ] Weather alerts sending
- [ ] Price alerts triggering
- [ ] Irrigation reminders

### ✅ Marketplace
- [ ] Real user listings
- [ ] Geolocation-based search
- [ ] Contact information
- [ ] Status updates

---

## 🚀 PERFORMANCE OPTIMIZATION

### Caching Strategy
```python
from functools import lru_cache
from datetime import datetime, timedelta

# Cache weather data for 1 hour
@lru_cache(maxsize=100)
def get_cached_weather(location, hour):
    return weather_service.get_current_weather(location)

def get_weather_with_cache(location):
    current_hour = datetime.now().hour
    return get_cached_weather(location, current_hour)
```

### Database Indexing
```python
# Add indexes for faster queries
with app.app_context():
    db.engine.execute('CREATE INDEX idx_user_location ON user(location)')
    db.engine.execute('CREATE INDEX idx_expense_user_date ON expense(user_id, date)')
    db.engine.execute('CREATE INDEX idx_soil_user ON soil_data(user_id)')
```

---

## 📊 MONITORING & LOGGING

### Add comprehensive logging
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.FileHandler('logs/api_calls.log'),
        logging.StreamHandler()
    ]
)

# Log all API calls
def log_api_call(service, endpoint, status):
    logger.info(f"API Call: {service} - {endpoint} - Status: {status}")
```

---

## 💰 COST ESTIMATION

### Free Tier Limits:
- OpenWeatherMap: 1,000 calls/day (FREE)
- Data.gov.in: Unlimited (FREE)
- Plant.id: 100 calls/month (FREE)
- Twilio: $15 credit (FREE trial)
- NASA POWER: Unlimited (FREE)

### Paid Options (if needed):
- OpenWeatherMap Pro: $40/month (60,000 calls/day)
- Plant.id Pro: $29/month (500 calls)
- Twilio: $0.0075 per SMS
- AWS Rekognition: $1 per 1000 images

---

## 🎓 TRAINING RESOURCES

### Datasets:
1. Crop Recommendation: https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset
2. Plant Disease: https://www.kaggle.com/datasets/vipoooool/new-plant-diseases-dataset
3. Crop Production: https://data.gov.in/catalog/crop-production-statistics
4. Weather Historical: https://www.ncei.noaa.gov/

### APIs:
1. OpenWeatherMap: https://openweathermap.org/api
2. Data.gov.in: https://data.gov.in/
3. Plant.id: https://web.plant.id/
4. NASA POWER: https://power.larc.nasa.gov/
5. Agmarknet: https://agmarknet.gov.in/

---

## 🐛 TROUBLESHOOTING

### Common Issues:

**1. API Key Not Working**
```bash
# Check if .env is loaded
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('OPENWEATHER_API_KEY'))"
```

**2. Model Not Found**
```bash
# Check if models directory exists
mkdir -p models
# Re-train models
python train_real_crop_model.py
```

**3. Database Errors**
```bash
# Reset database
rm instance/crop_advisory.db
python
>>> from app import app, db
>>> with app.app_context():
>>>     db.create_all()
```

**4. Import Errors**
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

---

## 📝 NEXT STEPS

1. **Week 1**: Setup APIs and train models
2. **Week 2**: Integrate real data services
3. **Week 3**: Test all features thoroughly
4. **Week 4**: Deploy and monitor

---

## 🎯 SUCCESS METRICS

- 0% static/hardcoded data
- 100% real API-driven features
- >85% ML model accuracy
- <2 second API response time
- 99% uptime

---

## 📞 SUPPORT

If you encounter issues:
1. Check logs: `tail -f logs/app.log`
2. Test APIs individually
3. Verify API keys in .env
4. Check internet connectivity
5. Review error messages

---

**REMEMBER**: Start with Phase 1 (API keys) and work sequentially. Don't skip phases!
