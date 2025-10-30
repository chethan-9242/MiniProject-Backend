from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List
import os
from dotenv import load_dotenv
import requests

load_dotenv()
router = APIRouter()

# Read API key lazily so changes to .env on restart are picked up

def get_api_key() -> str:
    return os.getenv("YOUTUBE_API_KEY", "").strip()

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
    embed_url: str | None = None

class YouTubeSearchResponse(BaseModel):
    videos: List[YouTubeVideo]
    total: int
    search_query: str | None = None

@router.get("/search", response_model=YouTubeSearchResponse)
async def search_youtube_videos(
    condition: str = Query(..., description="Disease/condition name to search"),
    max_results: int = Query(5, ge=1, le=10, description="Maximum number of results")
):
    """
    Search YouTube for ayurvedic treatment videos related to a condition.
    Uses API key if configured; otherwise returns offline-safe placeholders.
    """
    
    api_key = get_api_key()

    # Fallback placeholders (offline-safe: data URI thumbnails)
    if not api_key:
        svg = (
            "data:image/svg+xml;utf8," +
            "<svg xmlns='http://www.w3.org/2000/svg' width='320' height='180'>" +
            "<rect width='100%' height='100%' fill='%234CAF50'/><text x='50%' y='50%' dominant-baseline='middle' text-anchor='middle' fill='white' font-size='16'>Ayurvedic Video</text></svg>"
        )
        return {
            "videos": [
                {
                    "video_id": "",
                    "title": f"Ayurvedic Treatment for {condition}",
                    "description": "Educational overview of traditional Ayurvedic remedies and practices.",
                    "thumbnail_url": svg,
                    "channel_title": "Ayurveda Health",
                    "published_at": "",
                    "duration": "",
                    "view_count": 0,
                    "like_count": 0,
                    "relevance_note": f"Educational content related to {condition}",
                    "embed_url": None,
                }
            ],
            "total": 1,
            "search_query": f"ayurvedic treatment {condition} natural remedies",
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
                "key": api_key,
                "relevanceLanguage": "en",
                "safeSearch": "strict",
            },
            timeout=10,
        )
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=f"YouTube API error: {response.text}")

        data = response.json()
        ids = [item["id"].get("videoId") for item in data.get("items", []) if item.get("id", {}).get("videoId")]
        videos: list[dict] = []

        if ids:
            # Fetch statistics and durations
            details_resp = requests.get(
                "https://www.googleapis.com/youtube/v3/videos",
                params={
                    "part": "contentDetails,statistics,snippet",
                    "id": ",".join(ids),
                    "key": api_key,
                },
                timeout=10,
            )
            if details_resp.status_code != 200:
                raise HTTPException(status_code=details_resp.status_code, detail=f"YouTube API error: {details_resp.text}")
            details = {item["id"]: item for item in details_resp.json().get("items", [])}

            for item in data.get("items", []):
                vid = item["id"]["videoId"]
                snip = details.get(vid, {}).get("snippet", item.get("snippet", {}))
                stats = details.get(vid, {}).get("statistics", {})
                content = details.get(vid, {}).get("contentDetails", {})

                videos.append({
                    "video_id": vid,
                    "title": snip.get("title", ""),
                    "description": snip.get("description", ""),
                    "thumbnail_url": f"https://i.ytimg.com/vi/{vid}/mqdefault.jpg",
                    "channel_title": snip.get("channelTitle", ""),
                    "published_at": snip.get("publishedAt", ""),
                    "duration": content.get("duration", ""),
                    "view_count": int(stats.get("viewCount", 0)) if stats.get("viewCount") else 0,
                    "like_count": int(stats.get("likeCount", 0)) if stats.get("likeCount") else 0,
                    "relevance_note": f"Video about {condition} and Ayurvedic treatment approaches",
                    "embed_url": f"https://www.youtube-nocookie.com/embed/{vid}",
                })

        return {"videos": videos, "total": len(videos), "search_query": search_query}

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error fetching YouTube videos: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.get("/health")
async def health_check():
    """Check if YouTube API is configured"""
    api_key = get_api_key()
    return {
        "status": "healthy",
        "api_configured": bool(api_key),
        "message": "YouTube API key is configured" if api_key else "YouTube API key not configured - using demo placeholders",
    }
