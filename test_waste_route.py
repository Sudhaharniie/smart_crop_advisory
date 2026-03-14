"""Test script to verify waste management route"""
import sys
sys.path.insert(0, 'd:\\agri project new\\project agri')

from app import app

with app.test_client() as client:
    # Test without login
    print("Testing /waste-management without login...")
    response = client.get('/waste-management')
    print(f"Status: {response.status_code}")
    print(f"Redirects to: {response.location if response.status_code == 302 else 'N/A'}")
    
    # Test with mock session
    with client.session_transaction() as sess:
        sess['user_id'] = 1
        sess['username'] = 'test'
    
    print("\nTesting /waste-management with login...")
    response = client.get('/waste-management')
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("[OK] Page loads successfully!")
        print(f"Content length: {len(response.data)} bytes")
        # Check if key elements are present
        content = response.data.decode('utf-8')
        if 'Waste Management' in content:
            print("[OK] Title found")
        if 'residueForm' in content:
            print("[OK] Residue form found")
        if 'compostRecipeForm' in content:
            print("[OK] Compost form found")
        if 'waste_management.js' in content:
            print("[OK] JavaScript file linked")
    else:
        print(f"[ERROR] Error: {response.status_code}")
        print(response.data.decode('utf-8')[:500])
    
    # Test API endpoint
    print("\nTesting /api/waste/dashboard...")
    response = client.get('/api/waste/dashboard')
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        import json
        data = json.loads(response.data)
        print(f"[OK] API works! Data: {data}")
    else:
        print(f"[ERROR] API Error: {response.data.decode('utf-8')}")
