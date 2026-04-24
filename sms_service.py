"""
SMS Service Module
Handles SMS notifications via Twilio
"""
import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# Try to import Twilio
try:
    from twilio.rest import Client
    TWILIO_AVAILABLE = True
except ImportError:
    TWILIO_AVAILABLE = False
    logger.warning("Twilio not installed. SMS features will be simulated.")

class SMSService:
    def __init__(self, account_sid=None, auth_token=None, phone_number=None):
        self.account_sid = account_sid or os.getenv('TWILIO_ACCOUNT_SID')
        self.auth_token = auth_token or os.getenv('TWILIO_AUTH_TOKEN')
        self.phone_number = phone_number or os.getenv('TWILIO_PHONE_NUMBER')
        
        if TWILIO_AVAILABLE and self.account_sid and self.auth_token:
            try:
                self.client = Client(self.account_sid, self.auth_token)
                self.enabled = True
                logger.info("SMS Service initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Twilio client: {e}")
                self.enabled = False
        else:
            self.enabled = False
            logger.warning("SMS Service running in simulation mode")
    
    def send_sms(self, to_number, message):
        """
        Send SMS to a phone number
        
        Args:
            to_number (str): Recipient phone number (with country code, e.g., +919876543210)
            message (str): Message content
            
        Returns:
            dict: Status and message
        """
        try:
            # Validate phone number format
            if not to_number.startswith('+'):
                to_number = '+91' + to_number  # Default to India
            
            if self.enabled:
                # Send real SMS via Twilio
                message_obj = self.client.messages.create(
                    body=message,
                    from_=self.phone_number,
                    to=to_number
                )
                logger.info(f"SMS sent successfully to {to_number}. SID: {message_obj.sid}")
                return {
                    'success': True,
                    'message': 'SMS sent successfully',
                    'sid': message_obj.sid,
                    'status': message_obj.status
                }
            else:
                # Simulation mode
                logger.info(f"[SIMULATED] SMS to {to_number}: {message}")
                return {
                    'success': True,
                    'message': 'SMS simulated (Twilio not configured)',
                    'simulated': True
                }
        
        except Exception as e:
            logger.error(f"Failed to send SMS to {to_number}: {e}")
            return {
                'success': False,
                'message': f'Failed to send SMS: {str(e)}',
                'error': str(e)
            }
    
    def send_weather_alert(self, to_number, weather_data):
        """Send weather alert SMS"""
        message = f"Weather Alert: {weather_data['description']}. Temp: {weather_data['temperature']}°C, Humidity: {weather_data['humidity']}%, Rainfall: {weather_data['rainfall']}mm. Plan your farming activities accordingly."
        return self.send_sms(to_number, message)
    
    def send_price_alert(self, to_number, crop, price, trend):
        """Send market price alert SMS"""
        trend_text = "increased" if trend == "up" else "decreased" if trend == "down" else "stable"
        message = f"Market Update: {crop.title()} price {trend_text} to ₹{price}/quintal. Check dashboard for details."
        return self.send_sms(to_number, message)
    
    def send_irrigation_reminder(self, to_number, soil_moisture):
        """Send irrigation reminder SMS"""
        message = f"Irrigation Alert: Soil moisture is {soil_moisture}%. Time to water your crops for optimal growth."
        return self.send_sms(to_number, message)
    
    def send_disease_alert(self, to_number, disease_name, severity):
        """Send disease detection alert SMS"""
        message = f"Disease Alert: {disease_name} detected with {severity} severity. Check dashboard for treatment recommendations."
        return self.send_sms(to_number, message)
    
    def send_harvest_reminder(self, to_number, crop, days_remaining):
        """Send harvest reminder SMS"""
        message = f"Harvest Reminder: Your {crop} crop is ready for harvest in {days_remaining} days. Prepare your equipment and labor."
        return self.send_sms(to_number, message)

# Initialize global SMS service
sms_service = SMSService()
