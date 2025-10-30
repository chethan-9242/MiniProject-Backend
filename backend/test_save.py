import requests
import json

url = "http://localhost:8000/api/symptoms"

# Step 1: Analyze symptoms
print("Step 1: Analyzing symptoms...")
check_response = requests.post(f"{url}/check", json={
    "symptoms": [
        {
            "id": "1",
            "name": "Headache",
            "severity": "moderate",
            "duration": "1-2 days"
        },
        {
            "id": "2",
            "name": "Stress",
            "severity": "moderate",
            "duration": "1-2 weeks"
        }
    ]
})

analysis = check_response.json()
print(f"✅ Analysis complete: {analysis['possible_conditions'][0]['name']}")

# Step 2: Save the analysis
print("\nStep 2: Saving analysis...")
save_response = requests.post(f"{url}/save", json={
    "user_id": "test_user",
    "symptoms": [
        {
            "id": "1",
            "name": "Headache",
            "severity": "moderate",
            "duration": "1-2 days"
        },
        {
            "id": "2",
            "name": "Stress",
            "severity": "moderate",
            "duration": "1-2 weeks"
        }
    ],
    "analysis": analysis,
    "notes": "Test save from API"
})

save_result = save_response.json()
print(f"✅ {save_result['message']}")
print(f"   Analysis ID: {save_result['analysis_id']}")

# Step 3: Retrieve history
print("\nStep 3: Retrieving saved analyses...")
history_response = requests.get(f"{url}/history/test_user")
history = history_response.json()
print(f"✅ Found {history['count']} saved analyses")

if history['count'] > 0:
    print("\nMost recent analysis:")
    latest = history['analyses'][0]
    print(f"   ID: {latest['id']}")
    print(f"   Timestamp: {latest['timestamp']}")
    print(f"   Symptoms: {', '.join([s['name'] for s in latest['symptoms']])}")
    print(f"   Condition: {latest['analysis']['possible_conditions'][0]['name']}")

print("\n✅ All tests passed!")
