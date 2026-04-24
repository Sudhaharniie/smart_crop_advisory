import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import app, db, User, recommend_crops, analyze_soil_data
from werkzeug.security import generate_password_hash

class TestCropAdvisory(unittest.TestCase):
    
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()
    
    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_crop_recommendation(self):
        """Test ML crop recommendation"""
        result = recommend_crops(25, 18, 180, 28, 65, 6.8, 100)
        self.assertEqual(len(result), 3)
        self.assertIn('crop', result[0])
        self.assertIn('confidence', result[0])
    
    def test_soil_analysis(self):
        """Test soil data analysis"""
        recommendations = analyze_soil_data(6.5, 25, 18, 180)
        self.assertIsInstance(recommendations, list)
        self.assertGreater(len(recommendations), 0)
    
    def test_login_page(self):
        """Test login page loads"""
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)
    
    def test_dashboard_redirect(self):
        """Test dashboard redirects when not logged in"""
        response = self.app.get('/dashboard')
        self.assertEqual(response.status_code, 302)
    
    def test_user_registration(self):
        """Test user can register"""
        with app.app_context():
            user = User(
                username='testuser',
                email='test@example.com',
                password_hash=generate_password_hash('password123'),
                farm_size=5.0,
                location='Test City'
            )
            db.session.add(user)
            db.session.commit()
            
            found_user = User.query.filter_by(username='testuser').first()
            self.assertIsNotNone(found_user)
            self.assertEqual(found_user.email, 'test@example.com')

if __name__ == '__main__':
    unittest.main()
