import requests
import json

# Test data - Multiple test cases
test_cases = [
    {
        "name": "Single Symptom: Constipation",
        "symptoms": [
            {
                "id": "1",
                "name": "Constipation",
                "severity": "moderate",
                "duration": "3-7 days"
            }
        ]
    },
    {
        "name": "Single Symptom: Fever",
        "symptoms": [
            {
                "id": "1",
                "name": "Fever",
                "severity": "severe",
                "duration": "1-2 days"
            }
        ]
    },
    {
        "name": "Cold Symptoms",
        "symptoms": [
            {
                "id": "1",
                "name": "Cough",
                "severity": "moderate",
                "duration": "3-7 days"
            },
            {
                "id": "2",
                "name": "Sore Throat",
                "severity": "mild",
                "duration": "1-2 days"
            },
            {
                "id": "3",
                "name": "Congestion",
                "severity": "moderate",
                "duration": "3-7 days"
            }
        ]
    },
    {
        "name": "Headache & Stress Test",
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
    },
    {
        "name": "Digestive Issues Test",
        "symptoms": [
            {
                "id": "1",
                "name": "Bloating",
                "severity": "moderate",
                "duration": "1-2 days"
            },
            {
                "id": "2",
                "name": "Gas",
                "severity": "mild",
                "duration": "1-2 days"
            },
            {
                "id": "3",
                "name": "Stomach Pain",
                "severity": "moderate",
                "duration": "1-2 days"
            }
        ]
    }
]

# API endpoint
url = "http://localhost:8000/api/symptoms/check"

print("Testing Symptom Checker API...")
print(f"Endpoint: {url}")
print("\n" + "="*80)

# Test each case
for test_case in test_cases:
    print(f"\n🧪 TEST: {test_case['name']}")
    print("="*80)
    
    test_data = {"symptoms": test_case["symptoms"]}
    
    print(f"\nSymptoms:")
    for symptom in test_case["symptoms"]:
        print(f"  • {symptom['name']} ({symptom['severity']}, {symptom['duration']})")
    
    try:
        # Make POST request
        response = requests.post(url, json=test_data)
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"\n✅ Dosha Imbalance: {result['dosha_imbalance']['primary']}")
            print(f"   {result['dosha_imbalance']['description']}")
            
            print("\n📋 Possible Conditions:")
            for i, condition in enumerate(result['possible_conditions'], 1):
                print(f"   {i}. {condition['name']} ({condition['probability']}% match)")
                print(f"      {condition['ayurvedic_perspective']}")
            
            print("\n⚡ Immediate Actions:")
            for action in result['recommendations']['immediate_actions'][:2]:
                print(f"   • {action}")
            
            print("\n🌿 Herbal Remedies:")
            for herb in result['recommendations']['herbal_remedies'][:2]:
                print(f"   • {herb}")
                
        else:
            print(f"\n❌ Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("\n❌ Could not connect to the API. Make sure the backend is running on http://localhost:8000")
        break
    except Exception as e:
        print(f"\n❌ Error: {e}")
    
    print("\n" + "-"*80)
