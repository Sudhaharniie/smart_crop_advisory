"""
Free SMS Service using Email-to-SMS Gateway
No cost alternative to Twilio!
"""
import os
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logger = logging.getLogger(__name__)

class FreeSMSService:
    """
    Free SMS service using carrier email-to-SMS gateways
    Supports major carriers in India and worldwide
    """
    
    # Email-to-SMS gateways for major carriers
    CARRIER_GATEWAYS = {
        # India
        'airtel': 'airtelmail.com',
        'vodafone': 'vodafone.com',
        'idea': 'ideacellular.net',
        'jio': 'jio.com',
        'bsnl': 'bsnl.net',
        
        # USA (for reference)
        'att': 'txt.att.net',
        'tmobile': 'tmomail.net',
        'verizon': 'vtext.com',
        'sprint': 'messaging.sprintpcs.com'
    }
    
    def __init__(self):
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', 587))
        self.smtp_email = os.getenv('SMTP_EMAIL', '')
        self.smtp_password = os.getenv('SMTP_PASSWORD', '')
        self.enabled = bool(self.smtp_email and self.smtp_password)
        
        if not self.enabled:
            logger.warning("Free SMS not configured. Add SMTP credentials to .env")
    
    def send_sms(self, phone_number, message, carrier='airtel'):
        """
        Send SMS via email-to-SMS gateway (FREE!)
        
        Args:
            phone_number (str): 10-digit phone number
            message (str): SMS message (max 160 chars)
            carrier (str): Carrier name (airtel, vodafone, jio, etc.)
        
        Returns:
            dict: Result with success status
        """
        if not self.enabled:
            logger.info(f"[SIMULATED SMS] To: {phone_number}, Message: {message}")
            return {
                'success': True,
                'message': 'SMS simulated (configure SMTP for real SMS)',
                'simulated': True
            }
        
        try:
            # Clean phone number
            phone = phone_number.replace('+91', '').replace('-', '').replace(' ', '')
            
            # Get carrier gateway
            gateway = self.CARRIER_GATEWAYS.get(carrier.lower(), 'airtelmail.com')
            
            # Create email address
            to_email = f"{phone}@{gateway}"
            
            # Truncate message to 160 characters
            sms_message = message[:160]
            
            # Create email
            msg = MIMEMultipart()
            msg['From'] = self.smtp_email
            msg['To'] = to_email
            msg['Subject'] = ''  # No subject for SMS
            
            msg.attach(MIMEText(sms_message, 'plain'))
            
            # Send via SMTP
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_email, self.smtp_password)
                server.send_message(msg)
            
            logger.info(f"✅ FREE SMS sent to {phone_number} via {carrier}")
            
            return {
                'success': True,
                'message': f'SMS sent to {phone_number}',
                'method': 'email-to-sms',
                'carrier': carrier
            }
        
        except Exception as e:
            logger.error(f"Failed to send SMS: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to send SMS'
            }
    
    def send_weather_alert(self, phone_number, weather_data, carrier='airtel'):
        """Send weather alert SMS"""
        message = f"Weather Alert: {weather_data.get('description', 'N/A')}, Temp: {weather_data.get('temperature', 'N/A')}°C, Humidity: {weather_data.get('humidity', 'N/A')}%"
        return self.send_sms(phone_number, message, carrier)
    
    def send_irrigation_reminder(self, phone_number, moisture_level, carrier='airtel'):
        """Send irrigation reminder SMS"""
        if moisture_level < 50:
            message = f"Irrigation Alert: Soil moisture is {moisture_level}%. Water your crops today!"
        else:
            message = f"Irrigation Update: Soil moisture is {moisture_level}%. No watering needed."
        return self.send_sms(phone_number, message, carrier)
    
    def send_price_alert(self, phone_number, crop, price, change, carrier='airtel'):
        """Send market price alert SMS"""
        direction = "increased" if change > 0 else "decreased"
        message = f"Price Alert: {crop.title()} {direction} to ₹{price}/quintal ({abs(change)}%)"
        return self.send_sms(phone_number, message, carrier)
    
    def send_disease_alert(self, phone_number, disease, severity, carrier='airtel'):
        """Send disease detection alert SMS"""
        message = f"Disease Alert: {disease} detected ({severity} severity). Check dashboard for treatment."
        return self.send_sms(phone_number, message, carrier)

# Initialize free SMS service
free_sms_service = FreeSMSService()
