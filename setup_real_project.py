"""
Quick Setup Script for Real & Dynamic Project
Run this to automatically configure your project
"""

import os
import sys

def create_env_file():
    """Create .env file with placeholders"""
    env_content = """# Flask Configuration
SECRET_KEY=change-this-to-random-secret-key
DATABASE_URL=sqlite:///crop_advisory.db

# Weather API (OpenWeatherMap)
# Sign up: https://openweathermap.org/api
OPENWEATHER_API_KEY=your_openweather_api_key_here

# Market Data (Data.gov.in)
# Sign up: https://data.gov.in/
DATA_GOV_IN_KEY=your_data_gov_in_key_here
AGMARKNET_API_KEY=your_agmarknet_key_here

# Disease Detection (Plant.id)
# Sign up: https://web.plant.id/
PLANTID_API_KEY=your_plantid_api_key_here

# SMS Service (Twilio)
# Sign up: https://www.twilio.com/
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=+1234567890

# IoT Sensors (Optional)
IOT_SENSOR_ENDPOINT=http://192.168.1.100:8080

# NASA POWER API (No key needed - Free)
# Automatically used for satellite data
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ .env file created")
    print("⚠️  IMPORTANT: Edit .env and add your real API keys!")

def create_directories():
    """Create necessary directories"""
    dirs = ['models', 'data', 'logs', 'static/uploads', 'static/audio']
    
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
        print(f"✅ Created directory: {dir_path}")

def install_dependencies():
    """Install required packages"""
    print("\n📦 Installing dependencies...")
    print("This may take a few minutes...\n")
    
    packages = [
        'flask',
        'flask-sqlalchemy',
        'requests',
        'pandas',
        'numpy',
        'scikit-learn',
        'pillow',
        'geopy',
        'twilio',
        'python-dotenv',
        'joblib',
        'reportlab',
        'gtts',
        'werkzeug'
    ]
    
    for package in packages:
        os.system(f'pip install {package}')
    
    print("\n✅ All dependencies installed")

def download_sample_data():
    """Download sample datasets"""
    print("\n📥 Downloading sample datasets...")
    
    # Create data directory
    os.makedirs('data', exist_ok=True)
    
    print("⚠️  Manual step required:")
    print("1. Download Crop Recommendation Dataset:")
    print("   https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset")
    print("2. Save as: data/Crop_recommendation.csv")
    print("\n3. Download Plant Disease Dataset (optional):")
    print("   https://www.kaggle.com/datasets/vipoooool/new-plant-diseases-dataset")
    print("4. Extract to: data/PlantVillage/")

def create_training_script():
    """Create model training script"""
    script_content = """
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

print("Training Real Crop Recommendation Model...")

# Check if data exists
if not os.path.exists('data/Crop_recommendation.csv'):
    print("ERROR: Dataset not found!")
    print("Download from: https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset")
    print("Save as: data/Crop_recommendation.csv")
    exit(1)

# Load dataset
df = pd.read_csv('data/Crop_recommendation.csv')
print(f"Dataset loaded: {len(df)} samples")

# Prepare features
X = df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
y = df['label']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
print("Training model...")
model = RandomForestClassifier(n_estimators=200, random_state=42, max_depth=20)
model.fit(X_train, y_train)

# Evaluate
accuracy = model.score(X_test, y_test)
print(f"Model Accuracy: {accuracy * 100:.2f}%")

# Save model
os.makedirs('models', exist_ok=True)
joblib.dump(model, 'models/crop_recommendation_real.pkl')
print("✅ Model saved to: models/crop_recommendation_real.pkl")

print("\\nModel is ready to use!")
"""
    
    with open('train_model.py', 'w') as f:
        f.write(script_content)
    
    print("✅ Created train_model.py")

def test_apis():
    """Test API connections"""
    print("\n🧪 Testing API connections...")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    # Test OpenWeatherMap
    api_key = os.getenv('OPENWEATHER_API_KEY')
    if api_key and api_key != 'your_openweather_api_key_here':
        import requests
        try:
            response = requests.get(
                f"http://api.openweathermap.org/data/2.5/weather?q=Delhi&appid={api_key}",
                timeout=10
            )
            if response.status_code == 200:
                print("✅ OpenWeatherMap API: Working")
            else:
                print(f"❌ OpenWeatherMap API: Error {response.status_code}")
        except Exception as e:
            print(f"❌ OpenWeatherMap API: {e}")
    else:
        print("⚠️  OpenWeatherMap API: Key not configured")
    
    # Test Plant.id
    plantid_key = os.getenv('PLANTID_API_KEY')
    if plantid_key and plantid_key != 'your_plantid_api_key_here':
        print("✅ Plant.id API: Key configured")
    else:
        print("⚠️  Plant.id API: Key not configured")
    
    # Test Twilio
    twilio_sid = os.getenv('TWILIO_ACCOUNT_SID')
    if twilio_sid and twilio_sid != 'your_twilio_account_sid':
        print("✅ Twilio SMS: Configured")
    else:
        print("⚠️  Twilio SMS: Not configured")

def print_next_steps():
    """Print next steps for user"""
    print("\n" + "="*60)
    print("🎉 SETUP COMPLETE!")
    print("="*60)
    
    print("\n📋 NEXT STEPS:\n")
    
    print("1. Configure API Keys:")
    print("   - Edit .env file")
    print("   - Add your real API keys")
    print("   - Save the file")
    
    print("\n2. Download Datasets:")
    print("   - Get Crop Recommendation dataset")
    print("   - Save to data/Crop_recommendation.csv")
    
    print("\n3. Train ML Model:")
    print("   python train_model.py")
    
    print("\n4. Run Application:")
    print("   python app.py")
    
    print("\n5. Test Features:")
    print("   - Open http://localhost:5000")
    print("   - Register/Login")
    print("   - Test weather, crops, prices")
    
    print("\n📚 Documentation:")
    print("   - Read: REAL_PROJECT_SETUP_GUIDE.md")
    print("   - Check: real_data_integration.py")
    
    print("\n💡 Tips:")
    print("   - Start with free API tiers")
    print("   - Test one feature at a time")
    print("   - Check logs/app.log for errors")
    
    print("\n" + "="*60)

def main():
    """Main setup function"""
    print("="*60)
    print("🚀 SMART CROP ADVISORY - REAL DATA SETUP")
    print("="*60)
    
    print("\nThis script will:")
    print("1. Create .env file for API keys")
    print("2. Create necessary directories")
    print("3. Install Python dependencies")
    print("4. Create training scripts")
    print("5. Test API connections")
    
    input("\nPress Enter to continue...")
    
    # Run setup steps
    create_env_file()
    create_directories()
    
    print("\n" + "="*60)
    install_choice = input("Install dependencies now? (y/n): ")
    if install_choice.lower() == 'y':
        install_dependencies()
    else:
        print("⚠️  Skipped dependency installation")
        print("   Run manually: pip install -r requirements.txt")
    
    download_sample_data()
    create_training_script()
    
    print("\n" + "="*60)
    test_choice = input("Test API connections now? (y/n): ")
    if test_choice.lower() == 'y':
        test_apis()
    else:
        print("⚠️  Skipped API testing")
    
    print_next_steps()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Setup failed: {e}")
        sys.exit(1)
