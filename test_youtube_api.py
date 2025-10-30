#!/usr/bin/env python3
"""
Test script for YouTube API integration
"""

import requests
import json
from typing import Dict, Any

def test_youtube_api():
    """Test the YouTube API endpoints"""
    base_url = "http://localhost:8000/api/youtube"
    
    print("🧪 Testing YouTube API Integration...")
    print("=" * 50)
    
    # Test 1: Health check
    try:
        print("\n1. Testing health endpoint...")
        response = requests.get(f"{base_url}/health")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.json()}")
            print("   ✅ Health check passed")
        else:
            print("   ❌ Health check failed")
    except Exception as e:
        print(f"   ❌ Health check error: {e}")
    
    # Test 2: Get supported conditions
    try:
        print("\n2. Testing conditions endpoint...")
        response = requests.get(f"{base_url}/conditions")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Found {len(data.get('supported_conditions', []))} conditions")
            print("   ✅ Conditions endpoint working")
        else:
            print("   ❌ Conditions endpoint failed")
    except Exception as e:
        print(f"   ❌ Conditions endpoint error: {e}")
    
    # Test 3: Search for videos
    test_conditions = ["acne", "hair loss", "eczema"]
    
    for condition in test_conditions:
        try:
            print(f"\n3. Testing search for '{condition}'...")
            response = requests.get(f"{base_url}/search", params={
                "condition": condition,
                "max_results": 3
            })
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                videos = data.get("videos", [])
                print(f"   Found {len(videos)} videos")
                print(f"   Search query used: '{data.get('search_query', 'N/A')}'")
                
                if videos:
                    first_video = videos[0]
                    print(f"   First video: '{first_video.get('title', 'N/A')[:50]}...'")
                    print(f"   Channel: {first_video.get('channel_title', 'N/A')}")
                    print(f"   Views: {first_video.get('view_count', 'N/A')}")
                    print("   ✅ Search working")
                else:
                    print("   ⚠️  No videos found")
            else:
                print("   ❌ Search failed")
                print(f"   Error: {response.text}")
        except Exception as e:
            print(f"   ❌ Search error: {e}")
    
    # Test 4: Test error handling
    try:
        print("\n4. Testing error handling with empty condition...")
        response = requests.get(f"{base_url}/search", params={"condition": ""})
        print(f"   Status: {response.status_code}")
        if response.status_code == 400:
            print("   ✅ Error handling working correctly")
        else:
            print("   ⚠️  Expected 400 status code for empty condition")
    except Exception as e:
        print(f"   ❌ Error handling test failed: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 YouTube API testing completed!")

def test_frontend_integration():
    """Test if frontend can connect to backend"""
    print("\n🌐 Testing Frontend Integration...")
    print("=" * 50)
    
    # This would typically be run from the browser console or a separate frontend test
    print("   ℹ️  To test frontend integration:")
    print("   1. Start the backend server: uvicorn main:app --reload")
    print("   2. Start the frontend: npm start")
    print("   3. Navigate to Hair & Scalp Disorders module")
    print("   4. Complete an analysis to see YouTube videos appear")
    print("   5. Check browser console for any CORS or API errors")

if __name__ == "__main__":
    test_youtube_api()
    test_frontend_integration()