import requests
import json

url = "http://localhost:8000/api/symptoms/check"

test_data = {
    "symptoms": [
        {
            "id": "1",
            "name": "Constipation",
            "severity": "moderate",
            "duration": "3-7 days"
        }
    ]
}

response = requests.post(url, json=test_data)
result = response.json()

print("Input: Constipation")
print("\nAll Conditions Found:")
for i, condition in enumerate(result['possible_conditions'], 1):
    print(f"{i}. {condition['name']} - {condition['probability']}%")

print(f"\nSelected Dosha: {result['dosha_imbalance']['primary']}")
print(f"\nRecommendations:")
print("Immediate Actions:")
for action in result['recommendations']['immediate_actions']:
    print(f"  • {action}")
