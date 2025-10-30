# YouTube Integration for Ayurvedic Treatment Videos

This document explains how to use and customize the YouTube integration in your SwasthVedha application.

## Overview

The YouTube integration fetches and displays educational Ayurvedic treatment videos related to diagnosed skin or hair conditions. It consists of:

- **Backend API** (`youtube_integration.py`) - Handles YouTube Data API v3 calls
- **Frontend Component** (`YouTubeVideos.tsx`) - Displays videos with player and metadata
- **Integration** - Automatically shows relevant videos after condition analysis

## Features

### Backend Features
- ✅ YouTube Data API v3 integration
- ✅ Intelligent search queries with Ayurvedic terminology
- ✅ Quality filtering (view count, like count)
- ✅ Mock data fallback when API is unavailable
- ✅ Error handling and rate limiting
- ✅ Configurable search parameters

### Frontend Features
- ✅ Embedded video player with iframe
- ✅ Video metadata display (title, description, stats)
- ✅ Thumbnail previews with hover effects
- ✅ Video selection and playlist functionality
- ✅ Loading states and error handling
- ✅ Responsive design
- ✅ Educational disclaimers

## Backend API Endpoints

### 1. Search Videos
```http
GET /api/youtube/search?condition={condition}&max_results={max_results}
```

**Parameters:**
- `condition` (required): Health condition to search for
- `max_results` (optional): Number of videos to return (default: 5, max: 10)

**Response:**
```json
{
  "videos": [
    {
      "title": "Video Title",
      "description": "Video description...",
      "video_id": "dQw4w9WgXcQ",
      "view_count": 1000000,
      "like_count": 50000,
      "thumbnail_url": "https://img.youtube.com/vi/dQw4w9WgXcQ/maxresdefault.jpg",
      "embed_url": "https://www.youtube.com/embed/dQw4w9WgXcQ",
      "relevance_note": "Why this video is relevant...",
      "duration": "10:30",
      "published_at": "2023-01-15T10:30:00Z",
      "channel_title": "Channel Name"
    }
  ],
  "search_query": "ayurveda acne treatment natural remedies",
  "total_results": 5
}
```

### 2. Get Supported Conditions
```http
GET /api/youtube/conditions
```

**Response:**
```json
{
  "supported_conditions": [
    "acne", "eczema", "psoriasis", "hair loss", "dandruff", ...
  ]
}
```

### 3. Health Check
```http
GET /api/youtube/health
```

**Response:**
```json
{
  "status": "healthy",
  "api_available": true,
  "timestamp": "2023-12-10T15:30:45Z"
}
```

## Frontend Usage

### Basic Usage

```tsx
import YouTubeVideos from './components/YouTubeVideos';

function MyComponent() {
  return (
    <YouTubeVideos 
      condition="acne"
      maxResults={5}
      showEmbeddedPlayer={true}
    />
  );
}
```

### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `condition` | string | required | Health condition to search for |
| `maxResults` | number | 5 | Number of videos to fetch (max 10) |
| `showEmbeddedPlayer` | boolean | true | Show embedded video player |

### Integration Examples

#### 1. In Analysis Results (Current Implementation)
```tsx
// After diagnosis is complete
{result && (
  <div className="bg-white rounded-2xl shadow-lg p-6">
    <YouTubeVideos 
      condition={result.detected_condition}
      maxResults={5}
      showEmbeddedPlayer={true}
    />
  </div>
)}
```

#### 2. Standalone Search Page
```tsx
// Dedicated video search page
<YouTubeVideos 
  condition={searchTerm}
  maxResults={8}
  showEmbeddedPlayer={true}
/>
```

#### 3. Compact List View
```tsx
// Without embedded player
<YouTubeVideos 
  condition="eczema"
  maxResults={3}
  showEmbeddedPlayer={false}
/>
```

## Configuration

### Backend Configuration

1. **YouTube API Key**
   ```python
   # In backend/main.py or environment
   YOUTUBE_API_KEY = "your-youtube-api-key-here"
   ```

2. **Search Parameters**
   ```python
   # In youtube_integration.py
   DEFAULT_MAX_RESULTS = 5
   SEARCH_TERMS = {
       "acne": "ayurveda acne treatment natural remedies skincare",
       "eczema": "ayurvedic eczema treatment natural dermatitis cure",
       # Add more mappings...
   }
   ```

3. **Rate Limiting**
   ```python
   # YouTube API quota limits
   DAILY_QUOTA_LIMIT = 10000  # YouTube API units per day
   SEARCHES_PER_HOUR = 100    # Custom rate limit
   ```

### Frontend Configuration

1. **API Base URL**
   ```tsx
   // In YouTubeVideos.tsx
   const API_BASE_URL = "http://localhost:8000/api/youtube";
   ```

2. **Custom Styling**
   ```tsx
   // Customize colors in tailwind.config.js
   colors: {
     ayurveda: {
       50: '#f0f9f0',
       600: '#28802a',
       // ... other shades
     }
   }
   ```

## Testing

### 1. Backend Testing
```bash
# Run the test script
python test_youtube_api.py

# Or manual testing with curl
curl "http://localhost:8000/api/youtube/search?condition=acne&max_results=3"
```

### 2. Frontend Testing
```bash
# Start both servers
uvicorn main:app --reload  # Backend
npm start                  # Frontend

# Test in browser:
# 1. Go to Hair & Scalp Disorders
# 2. Upload image and analyze
# 3. Check if videos appear in results
# 4. Test video selection and playback
```

### 3. Error Testing
- Test with empty condition
- Test with invalid API key
- Test with network disconnection
- Test API quota exceeded

## Troubleshooting

### Common Issues

1. **No Videos Found**
   ```
   Cause: Invalid API key or quota exceeded
   Solution: Check API key and quota in Google Console
   ```

2. **CORS Errors**
   ```
   Cause: Backend not allowing frontend domain
   Solution: Add CORS middleware in FastAPI
   ```

3. **Videos Not Loading**
   ```
   Cause: Network issues or YouTube blocking
   Solution: Check network and use fallback data
   ```

4. **Quota Exceeded**
   ```
   Cause: Too many API calls
   Solution: Implement caching and rate limiting
   ```

### Debug Tips

1. **Check Backend Logs**
   ```bash
   # Enable debug logging
   uvicorn main:app --reload --log-level debug
   ```

2. **Check Frontend Console**
   ```javascript
   // Enable verbose logging
   localStorage.setItem('debug', 'youtube:*');
   ```

3. **Verify API Key**
   ```bash
   # Test API key directly
   curl "https://www.googleapis.com/youtube/v3/search?key=YOUR_KEY&q=test"
   ```

## Customization

### Adding New Conditions

1. **Backend - Add to search terms**
   ```python
   SEARCH_TERMS = {
       "acne": "ayurveda acne treatment natural remedies",
       "new_condition": "ayurveda new_condition treatment natural cure"
   }
   ```

2. **Frontend - Update condition list**
   ```tsx
   const popularConditions = [
     'Acne', 'Eczema', 'New Condition'
   ];
   ```

### Custom Search Logic

```python
def generate_search_query(condition: str) -> str:
    # Custom logic for search terms
    base_terms = "ayurveda treatment natural remedies"
    condition_specific = SEARCH_TERMS.get(condition, condition)
    return f"{base_terms} {condition_specific}"
```

### Video Filtering

```python
def filter_videos(videos: List[dict]) -> List[dict]:
    # Custom filtering logic
    return [
        video for video in videos 
        if video['view_count'] > 1000 and 
           'ayurveda' in video['title'].lower()
    ]
```

## Security Considerations

1. **API Key Protection**
   - Store in environment variables
   - Don't commit to version control
   - Use different keys for dev/prod

2. **Rate Limiting**
   - Implement backend rate limiting
   - Cache results to reduce API calls
   - Monitor quota usage

3. **Content Filtering**
   - Validate video content appropriateness
   - Filter out commercial/promotional content
   - Ensure educational focus

## Performance Optimization

1. **Caching**
   ```python
   # Cache search results
   @lru_cache(maxsize=100)
   def cached_video_search(condition: str):
       return search_videos(condition)
   ```

2. **Lazy Loading**
   ```tsx
   // Load videos only when needed
   useEffect(() => {
     if (condition && isVisible) {
       fetchVideos(condition);
     }
   }, [condition, isVisible]);
   ```

3. **Thumbnail Optimization**
   ```tsx
   // Use appropriate thumbnail sizes
   const thumbnailUrl = `https://img.youtube.com/vi/${videoId}/mqdefault.jpg`;
   ```

## Future Enhancements

- [ ] Video bookmarking/favorites
- [ ] User rating system for videos
- [ ] AI-powered content summarization
- [ ] Integration with other video platforms
- [ ] Offline video caching
- [ ] Multi-language support
- [ ] Advanced filtering options

## Support

For questions or issues with the YouTube integration:

1. Check this documentation first
2. Review the test script results
3. Check browser console for errors
4. Verify API key and quota status
5. Test with mock data to isolate issues

---

**Note**: This integration requires a valid YouTube Data API v3 key and respects YouTube's Terms of Service and API usage policies.