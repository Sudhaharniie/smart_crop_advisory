# SMS Alerts - Twilio Free Tier (500 SMS/month)
# Sign up: https://www.twilio.com/try-twilio

TWILIO_ENABLED = False  # Set True after adding credentials

def send_sms(phone, message):
    """Send SMS alert"""
    if not TWILIO_ENABLED:
        print(f"SMS to {phone}: {message}")
        return {'success': True, 'simulated': True}
    
    try:
        from twilio.rest import Client
        client = Client('YOUR_SID', 'YOUR_TOKEN')
        client.messages.create(body=message, from_='+1234567890', to=phone)
        return {'success': True, 'simulated': False}
    except:
        return {'success': False, 'simulated': False}
