"""
Test script for Advanced Symptoms Analysis
Run this to test the symptoms analysis system
"""

import asyncio
import sys
import json
from pathlib import Path

# Add the backend directory to Python path
sys.path.append(str(Path(__file__).parent))

from services.symptoms_analysis_service import get_symptoms_service

def test_basic_symptoms():
    """Test basic symptoms analysis"""
    print("🔬 Testing Basic Symptoms Analysis...")
    
    # Test symptoms data
    test_symptoms = [
        {"id": "1", "name": "headache", "severity": "moderate", "duration": "2 days"},
        {"id": "2", "name": "fever", "severity": "mild", "duration": "1 day"},
        {"id": "3", "name": "fatigue", "severity": "severe", "duration": "3 days"}
    ]
    
    # Get service and analyze
    service = get_symptoms_service()
    result = service.analyze_symptoms(test_symptoms)
    
    # Display results
    print(f"\n✅ Analysis Method: {result.get('analysis_method', 'unknown')}")
    print(f"✅ Confidence: {result.get('confidence', 0.0):.1%}")
    
    # Triage
    triage = result.get('triage', {})
    print(f"\n🚨 Triage Level: {triage.get('level', 'unknown').upper()}")
    print(f"   Action: {triage.get('action', 'No action specified')}")
    
    # Conditions
    conditions = result.get('possible_conditions', [])
    print(f"\n🩺 Possible Conditions ({len(conditions)}):")
    for i, condition in enumerate(conditions[:3], 1):
        print(f"   {i}. {condition.get('name', 'Unknown')} ({condition.get('probability', 0):.1f}%)")
        print(f"      {condition.get('description', 'No description')}")
    
    # Dosha analysis
    dosha = result.get('dosha_imbalance', {})
    print(f"\n🧘 Dosha Analysis:")
    print(f"   Primary: {dosha.get('primary', 'Unknown')}")
    print(f"   Description: {dosha.get('description', 'No description')}")
    
    # Recommendations
    recommendations = result.get('recommendations', {})
    immediate = recommendations.get('immediate_actions', [])
    if immediate:
        print(f"\n💊 Immediate Actions:")
        for action in immediate[:3]:
            print(f"   • {action}")
    
    return result

def test_emergency_symptoms():
    """Test emergency symptoms detection"""
    print("\n🚨 Testing Emergency Symptoms Detection...")
    
    emergency_symptoms = [
        {"id": "1", "name": "severe chest pain", "severity": "severe", "duration": "30 minutes"},
        {"id": "2", "name": "difficulty breathing", "severity": "severe", "duration": "1 hour"}
    ]
    
    service = get_symptoms_service()
    result = service.analyze_symptoms(emergency_symptoms)
    
    triage = result.get('triage', {})
    print(f"🚨 Triage Level: {triage.get('level', 'unknown').upper()}")
    print(f"   Emergency Detection: {'✅ WORKING' if triage.get('level') == 'emergency' else '❌ FAILED'}")
    
    return result

def test_dosha_inference():
    """Test dosha inference accuracy"""
    print("\n🧘 Testing Dosha Inference...")
    
    # Vata symptoms
    vata_symptoms = [
        {"id": "1", "name": "anxiety", "severity": "moderate", "duration": "1 week"},
        {"id": "2", "name": "insomnia", "severity": "moderate", "duration": "5 days"},
        {"id": "3", "name": "constipation", "severity": "mild", "duration": "3 days"}
    ]
    
    service = get_symptoms_service()
    result = service.analyze_symptoms(vata_symptoms)
    
    dosha = result.get('dosha_imbalance', {})
    primary_dosha = dosha.get('primary', '').lower()
    
    print(f"   Expected: Vata")
    print(f"   Detected: {dosha.get('primary', 'Unknown')}")
    print(f"   Accuracy: {'✅ CORRECT' if 'vata' in primary_dosha else '❌ INCORRECT'}")
    
    return result

def run_comprehensive_test():
    """Run comprehensive test suite"""
    print("🚀 Starting Comprehensive Symptoms Analysis Test\n")
    
    try:
        # Test 1: Basic functionality
        basic_result = test_basic_symptoms()
        
        # Test 2: Emergency detection
        emergency_result = test_emergency_symptoms()
        
        # Test 3: Dosha inference
        dosha_result = test_dosha_inference()
        
        # Summary
        print("\n" + "="*50)
        print("📊 TEST SUMMARY")
        print("="*50)
        
        tests_passed = 0
        total_tests = 3
        
        # Check basic analysis
        if basic_result.get('confidence', 0) > 0.5:
            print("✅ Basic Analysis: PASSED")
            tests_passed += 1
        else:
            print("❌ Basic Analysis: FAILED")
        
        # Check emergency detection
        if emergency_result.get('triage', {}).get('level') == 'emergency':
            print("✅ Emergency Detection: PASSED") 
            tests_passed += 1
        else:
            print("❌ Emergency Detection: FAILED")
        
        # Check dosha inference
        if 'vata' in dosha_result.get('dosha_imbalance', {}).get('primary', '').lower():
            print("✅ Dosha Inference: PASSED")
            tests_passed += 1
        else:
            print("❌ Dosha Inference: FAILED")
        
        print(f"\n🎯 Overall Score: {tests_passed}/{total_tests} ({tests_passed/total_tests*100:.0f}%)")
        
        if tests_passed == total_tests:
            print("🎉 ALL TESTS PASSED! Symptoms analysis is working correctly.")
        elif tests_passed >= 2:
            print("⚠️  Most tests passed. System is functional with minor issues.")
        else:
            print("❌ Multiple test failures. System needs attention.")
            
    except Exception as e:
        print(f"💥 Test failed with error: {str(e)}")
        print("This might indicate missing dependencies or configuration issues.")

if __name__ == "__main__":
    run_comprehensive_test()