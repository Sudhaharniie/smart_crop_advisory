import sys
sys.path.insert(0, 'd:\\agri project new\\project agri')

print("=" * 60)
print("WASTE MANAGEMENT FEATURE DIAGNOSTIC")
print("=" * 60)

# Test 1: Check if app loads
print("\n1. Loading Flask app...")
try:
    from app import app
    print("   [OK] App loaded successfully")
except Exception as e:
    print(f"   [ERROR] Failed to load app: {e}")
    sys.exit(1)

# Test 2: Check routes
print("\n2. Checking routes...")
routes = [str(rule) for rule in app.url_map.iter_rules()]
waste_routes = [r for r in routes if 'waste' in r.lower()]
print(f"   Found {len(waste_routes)} waste-related routes:")
for route in waste_routes:
    print(f"   - {route}")

# Test 3: Check if waste_management route exists
print("\n3. Checking /waste-management route...")
if '/waste-management' in routes:
    print("   [OK] Route exists")
else:
    print("   [ERROR] Route NOT found")

# Test 4: Check templates
print("\n4. Checking templates...")
import os
template_dir = 'd:\\agri project new\\project agri\\templates'
templates = os.listdir(template_dir)
waste_templates = [t for t in templates if 'waste' in t.lower()]
print(f"   Found {len(waste_templates)} waste-related templates:")
for t in waste_templates:
    print(f"   - {t}")

# Test 5: Check if waste_management.html exists
if 'waste_management.html' in templates:
    print("   [OK] waste_management.html exists")
else:
    print("   [ERROR] waste_management.html NOT found")

# Test 6: Test the route with mock session
print("\n5. Testing route with mock session...")
with app.test_client() as client:
    with client.session_transaction() as sess:
        sess['user_id'] = 1
        sess['username'] = 'test'
    
    response = client.get('/waste-management')
    print(f"   Status Code: {response.status_code}")
    
    if response.status_code == 200:
        print("   [OK] Route works!")
        content = response.data.decode('utf-8')
        
        # Check for key elements
        checks = {
            'Title': 'Waste Management' in content,
            'Residue Form': 'residueForm' in content,
            'Compost Form': 'compostRecipeForm' in content,
            'JavaScript': 'waste_management.js' in content
        }
        
        print("\n   Content checks:")
        for check, result in checks.items():
            status = "[OK]" if result else "[ERROR]"
            print(f"   {status} {check}: {'Found' if result else 'NOT FOUND'}")
    else:
        print(f"   [ERROR] Route failed with status {response.status_code}")

# Test 7: Check dashboard.html for waste management links
print("\n6. Checking dashboard.html for waste management links...")
dashboard_path = os.path.join(template_dir, 'dashboard.html')
with open(dashboard_path, 'r', encoding='utf-8') as f:
    dashboard_content = f.read()

link_count = dashboard_content.count('/waste-management')
print(f"   Found {link_count} links to /waste-management in dashboard.html")

# Find line numbers
lines = dashboard_content.split('\n')
link_lines = []
for i, line in enumerate(lines, 1):
    if '/waste-management' in line and '<!--' not in line:
        link_lines.append(i)

print(f"   Links found at lines: {link_lines}")

# Test 8: Check if links are visible (not hidden by CSS or comments)
print("\n7. Checking if links are visible...")
for line_num in link_lines:
    line = lines[line_num - 1]
    if 'display: none' in line or 'style="display:none"' in line:
        print(f"   [ERROR] Line {line_num} has display:none")
    elif '<!--' in line:
        print(f"   [ERROR] Line {line_num} is commented out")
    else:
        print(f"   [OK] Line {line_num} appears visible")
        print(f"      {line.strip()[:100]}...")

# Test 9: Check CSS for hiding
print("\n8. Checking CSS files...")
css_dir = 'd:\\agri project new\\project agri\\static\\css'
css_files = os.listdir(css_dir)
for css_file in css_files:
    css_path = os.path.join(css_dir, css_file)
    with open(css_path, 'r', encoding='utf-8') as f:
        css_content = f.read()
    if 'waste' in css_content.lower() or 'recycle' in css_content.lower():
        print(f"   Found waste/recycle reference in {css_file}")

print("\n" + "=" * 60)
print("DIAGNOSTIC COMPLETE")
print("=" * 60)
