from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
import os
import requests

router = APIRouter()

# Get YouTube API key from environment variable
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")

class YouTubeVideo(BaseModel):
    video_id: str
    title: str
    description: str
    thumbnail_url: str
    channel_title: str
    published_at: str
    duration: str = "N/A"
    view_count: int = 0
    like_count: int = 0
    relevance_note: str = "Educational video on Ayurvedic treatments"

class YouTubeSearchResponse(BaseModel):
    videos: List[YouTubeVideo]
    total: int

@router.get("/search", response_model=YouTubeSearchResponse)
async def search_youtube_videos(
    condition: str = Query(..., description="Disease/condition name to search"),
    max_results: int = Query(5, ge=1, le=10, description="Maximum number of results")
):
    """
    Search YouTube for ayurvedic treatment videos related to a condition
    
    If YouTube API key is not configured, returns demo/placeholder videos
    """
    
    # Check if API key is configured
    if not YOUTUBE_API_KEY:
        # Return placeholder videos if no API key
        return {
            "videos": [
                {
                    "video_id": "demo1",
                    "title": f"Ayurvedic Treatment for {condition}",
                    "description": "Natural remedies and herbal treatments for scalp and hair health. Learn about traditional Ayurvedic approaches to treating this condition.",
                    "thumbnail_url": "https://via.placeholder.com/320x180/4CAF50/FFFFFF?text=Ayurvedic+Treatment",
                    "channel_title": "Ayurveda Health Channel",
                    "published_at": "2024-01-01T00:00:00Z",
                    "duration": "10:25",
                    "view_count": 15000,
                    "like_count": 850,
                    "relevance_note": f"This video covers traditional Ayurvedic approaches to treating {condition} with herbal remedies and natural methods."
                },
                {
                    "video_id": "demo2",
                    "title": f"Home Remedies for {condition}",
                    "description": "Simple and effective home treatments using natural ingredients you can find in your kitchen. Step-by-step guide to natural healing.",
                    "thumbnail_url": "https://via.placeholder.com/320x180/2196F3/FFFFFF?text=Home+Remedies",
                    "channel_title": "Natural Health TV",
                    "published_at": "2024-02-15T00:00:00Z",
                    "duration": "8:15",
                    "view_count": 22000,
                    "like_count": 1200,
                    "relevance_note": f"Practical home remedies using common ingredients to help manage {condition} symptoms naturally."
                },
                {
                    "video_id": "demo3",
                    "title": f"Understanding {condition} - Ayurvedic Perspective",
                    "description": "Learn about causes, symptoms, and ayurvedic perspective on this condition. Expert insights and recommendations.",
                    "thumbnail_url": "https://via.placeholder.com/320x180/FF9800/FFFFFF?text=Expert+Guide",
                    "channel_title": "Health Education Network",
                    "published_at": "2024-03-20T00:00:00Z",
                    "duration": "12:40",
                    "view_count": 18500,
                    "like_count": 950,
                    "relevance_note": f"Comprehensive guide explaining {condition} from an Ayurvedic viewpoint with preventive measures."
                }
            ],
            "total": 3
        }
    
    try:
        # Search YouTube API
        search_query = f"ayurvedic treatment {condition} natural remedies"
        
        response = requests.get(
            "https://www.googleapis.com/youtube/v3/search",
            params={
                "part": "snippet",
                "q": search_query,
                "type": "video",
                "maxResults": max_results,
                "key": YOUTUBE_API_KEY,
                "relevanceLanguage": "en",
                "safeSearch": "strict"
            },
            timeout=10
        )
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"YouTube API error: {response.text}"
            )
        
        data = response.json()
        
        videos = []
        for item in data.get("items", []):
            video_id = item["id"].get("videoId")
            snippet = item.get("snippet", {})
            
            if video_id:
                videos.append({
                    "video_id": video_id,
                    "title": snippet.get("title", ""),
                    "description": snippet.get("description", ""),
                    "thumbnail_url": snippet.get("thumbnails", {}).get("medium", {}).get("url", ""),
                    "channel_title": snippet.get("channelTitle", ""),
                    "published_at": snippet.get("publishedAt", ""),
                    "duration": "N/A",
                    "view_count": 0,
                    "like_count": 0,
                    "relevance_note": f"Video about {condition} and Ayurvedic treatment approaches"
                })
        
        return {
            "videos": videos,
            "total": len(videos)
        }
    
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error fetching YouTube videos: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.get("/health")
async def health_check():
    """Check if YouTube API is configured"""
    return {
        "status": "healthy",
        "api_configured": bool(YOUTUBE_API_KEY),
        "message": "YouTube API key is configured" if YOUTUBE_API_KEY else "YouTube API key not configured - using demo videos"
    }
