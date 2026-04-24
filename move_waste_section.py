import re

# Read the dashboard file
with open('d:\\agri project new\\project agri\\templates\\dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and extract the waste management section
waste_start = content.find('<!-- WASTE MANAGEMENT SECTION - INTEGRATED -->')
waste_end = content.find('<!-- Overview -->', waste_start)

if waste_start == -1 or waste_end == -1:
    print("Could not find waste management section markers")
    exit(1)

waste_section = content[waste_start:waste_end]
print(f"Found waste management section: {len(waste_section)} characters")

# Remove waste management from current location
content_without_waste = content[:waste_start] + content[waste_end:]

# Find where to insert (after loan-insurance, before SMS alerts)
sms_marker = '<!-- SMS/WhatsApp Alerts -->'
insert_pos = content_without_waste.find(sms_marker)

if insert_pos == -1:
    print("Could not find SMS alerts marker")
    exit(1)

# Insert waste management section before SMS alerts
new_content = content_without_waste[:insert_pos] + waste_section + content_without_waste[insert_pos:]

# Write back
with open('d:\\agri project new\\project agri\\templates\\dashboard.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Successfully moved waste management section after loan-insurance!")
