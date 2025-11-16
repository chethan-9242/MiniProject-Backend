import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  Play, 
  Eye, 
  ThumbsUp, 
  Clock, 
  Calendar,
  ExternalLink,
  Loader2,
  AlertTriangle,
  RefreshCw
} from 'lucide-react';
import axios from 'axios';

const API_URL = (import.meta.env.VITE_API_URL || 'http://localhost:8000').replace(/\/$/, '');

interface YouTubeVideo {
  title: string;
  description: string;
  video_id: string;
  view_count: number;
  like_count: number;
  thumbnail_url: string;
  embed_url: string;
  relevance_note: string;
  duration: string;
  published_at: string;
  channel_title: string;
}

interface YouTubeVideosProps {
  condition: string;
  maxResults?: number;
  showEmbeddedPlayer?: boolean;
}

const YouTubeVideos: React.FC<YouTubeVideosProps> = ({ 
  condition, 
  maxResults = 5,
  showEmbeddedPlayer = true 
}) => {
  const [videos, setVideos] = useState<YouTubeVideo[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string>('');
  const [selectedVideo, setSelectedVideo] = useState<YouTubeVideo | null>(null);
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    if (condition.trim()) {
      fetchVideos(condition);
    }
  }, [condition]); // eslint-disable-line react-hooks/exhaustive-deps

  const fetchVideos = async (searchCondition: string) => {
    if (!searchCondition.trim()) return;

    setLoading(true);
    setError('');
    
    try {
      const response = await axios.get(`${API_URL}/api/youtube/search`, {
        params: {
          condition: searchCondition,
          max_results: maxResults
        }
      });

      setVideos(response.data.videos || []);
      setSearchQuery(response.data.search_query || '');
      
      // Auto-select first video for embedded player
      if (response.data.videos && response.data.videos.length > 0 && showEmbeddedPlayer) {
        setSelectedVideo(response.data.videos[0]);
      }
    } catch (err) {
      console.error('Error fetching YouTube videos:', err);
      setError('Failed to load Ayurvedic treatment videos. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const formatNumber = (num: number | undefined): string => {
    if (num === undefined || num === null) {
      return 'N/A';
    }
    if (num >= 1000000) {
      return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
      return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
  };

  const formatDate = (dateStr: string): string => {
    try {
      const date = new Date(dateStr);
      return date.toLocaleDateString('en-US', { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric' 
      });
    } catch {
      return 'N/A';
    }
  };

  const handleVideoSelect = (video: YouTubeVideo) => {
    console.log('Selecting video:', video.title, video.video_id);
    setSelectedVideo(video);
    
    // Scroll to top of embedded player
    if (showEmbeddedPlayer) {
      const playerElement = document.querySelector('[data-video-player]');
      if (playerElement) {
        playerElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    }
  };

  const openVideoInNewTab = (videoId: string) => {
    window.open(`https://www.youtube.com/watch?v=${videoId}`, '_blank');
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="h-8 w-8 animate-spin text-ayurveda-600" />
        <span className="ml-3 text-gray-600">Loading Ayurvedic treatment videos...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-2xl p-6">
        <div className="flex items-center mb-3">
          <AlertTriangle className="h-6 w-6 text-red-600 mr-3" />
          <h3 className="text-lg font-semibold text-red-800">Unable to Load Videos</h3>
        </div>
        <p className="text-red-700 mb-4">{error}</p>
        <button
          onClick={() => fetchVideos(condition)}
          className="flex items-center px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
        >
          <RefreshCw className="h-4 w-4 mr-2" />
          Try Again
        </button>
      </div>
    );
  }

  if (!videos.length) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-600 mb-4">No Ayurvedic treatment videos found for "{condition}"</p>
        <button
          onClick={() => fetchVideos(condition)}
          className="flex items-center mx-auto px-4 py-2 bg-ayurveda-600 text-white rounded-lg hover:bg-ayurveda-700 transition-colors"
        >
          <RefreshCw className="h-4 w-4 mr-2" />
          Search Again
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="text-center">
        <h3 className="text-2xl font-bold text-gray-900 mb-2">
          Ayurvedic Treatment Videos
        </h3>
        <p className="text-gray-600">
          Educational videos on traditional Ayurvedic remedies for {condition}
        </p>
        {searchQuery && (
          <p className="text-sm text-ayurveda-600 mt-2">
            Search query: "{searchQuery}"
          </p>
        )}
      </div>

      {/* Embedded Video Player */}
      {showEmbeddedPlayer && selectedVideo && (
        <motion.div
          key={selectedVideo.video_id}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="bg-white rounded-2xl shadow-lg overflow-hidden"
          data-video-player
        >
          <div className="aspect-video">
            {(() => {
              const embedSrc = `https://www.youtube-nocookie.com/embed/${selectedVideo.video_id}?rel=0&modestbranding=1&origin=${encodeURIComponent(window.location.origin)}`;
              return (
                <iframe
                  key={selectedVideo.video_id}
                  src={embedSrc}
                  title={selectedVideo.title}
                  className="w-full h-full"
                  frameBorder="0"
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                  allowFullScreen
                  sandbox="allow-same-origin allow-scripts allow-popups allow-presentation"
                  referrerPolicy="strict-origin-when-cross-origin"
                ></iframe>
              );
            })()}
          </div>
          <div className="p-6">
            <h4 className="text-xl font-semibold text-gray-900 mb-2">
              {selectedVideo.title}
            </h4>
            <div className="flex items-center space-x-4 text-sm text-gray-600 mb-3">
              <span className="flex items-center">
                <Eye className="h-4 w-4 mr-1" />
                {formatNumber(selectedVideo.view_count)} views
              </span>
              <span className="flex items-center">
                <ThumbsUp className="h-4 w-4 mr-1" />
                {formatNumber(selectedVideo.like_count)} likes
              </span>
              <span className="flex items-center">
                <Clock className="h-4 w-4 mr-1" />
                {selectedVideo.duration}
              </span>
            </div>
            <p className="text-gray-700 mb-3">{selectedVideo.description}</p>
            <div className="bg-ayurveda-50 rounded-lg p-4">
              <h5 className="font-semibold text-ayurveda-800 mb-2">Why this video is relevant:</h5>
              <p className="text-ayurveda-700 text-sm">{selectedVideo.relevance_note}</p>
            </div>
            <div className="flex justify-between items-center mt-4">
              <span className="text-sm text-gray-600">
                By {selectedVideo.channel_title} • {formatDate(selectedVideo.published_at)}
              </span>
              <button
                onClick={() => openVideoInNewTab(selectedVideo.video_id)}
                className="flex items-center text-ayurveda-600 hover:text-ayurveda-800 font-medium"
              >
                <ExternalLink className="h-4 w-4 mr-1" />
                Open in YouTube
              </button>
            </div>
          </div>
        </motion.div>
      )}

      {/* Video List */}
      <div className="grid gap-4">
        <h4 className="text-lg font-semibold text-gray-900">
          {showEmbeddedPlayer ? 'More Videos' : 'Recommended Videos'}
        </h4>
        {videos.map((video, index) => (
          <motion.div
            key={`video-${video.video_id}-${index}`}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            className={`bg-white rounded-xl shadow-lg overflow-hidden cursor-pointer transition-all duration-200 hover:shadow-xl ${
              selectedVideo?.video_id === video.video_id ? 'ring-2 ring-ayurveda-500' : ''
            }`}
            onClick={() => handleVideoSelect(video)}
          >
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {/* Thumbnail */}
              <div className="relative md:col-span-1">
                <img
                  src={video.thumbnail_url}
                  alt={video.title}
                  className="w-full h-48 md:h-full object-cover"
                />
                <div className="absolute inset-0 bg-black bg-opacity-30 flex items-center justify-center opacity-0 hover:opacity-100 transition-opacity">
                  <Play className="h-12 w-12 text-white" />
                </div>
                <div className="absolute bottom-2 right-2 bg-black bg-opacity-80 text-white px-2 py-1 rounded text-sm">
                  {video.duration}
                </div>
              </div>

              {/* Content */}
              <div className="p-4 md:col-span-2">
                <h5 className="text-lg font-semibold text-gray-900 mb-2 line-clamp-2">
                  {video.title}
                </h5>
                <p className="text-gray-600 text-sm mb-3 line-clamp-2">
                  {video.description}
                </p>
                
                {/* Stats */}
                <div className="flex items-center space-x-4 text-sm text-gray-500 mb-3">
                  <span className="flex items-center">
                    <Eye className="h-4 w-4 mr-1" />
                    {formatNumber(video.view_count)}
                  </span>
                  <span className="flex items-center">
                    <ThumbsUp className="h-4 w-4 mr-1" />
                    {formatNumber(video.like_count)}
                  </span>
                  <span className="flex items-center">
                    <Calendar className="h-4 w-4 mr-1" />
                    {formatDate(video.published_at)}
                  </span>
                </div>

                {/* Channel */}
                <p className="text-sm text-gray-600 mb-3">
                  By <span className="font-medium">{video.channel_title}</span>
                </p>

                {/* Relevance Note */}
                <div className="bg-ayurveda-50 rounded-lg p-3">
                  <p className="text-ayurveda-700 text-sm">{video.relevance_note}</p>
                </div>

                {/* Action Buttons */}
                <div className="flex space-x-3 mt-4">
                  {showEmbeddedPlayer && (
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        console.log('Watch Now clicked for:', video.title);
                        handleVideoSelect(video);
                      }}
                      className={`px-4 py-2 rounded-lg transition-colors flex items-center ${
                        selectedVideo?.video_id === video.video_id 
                          ? 'bg-ayurveda-700 text-white' 
                          : 'bg-ayurveda-600 text-white hover:bg-ayurveda-700'
                      }`}
                    >
                      <Play className="h-4 w-4 mr-2" />
                      {selectedVideo?.video_id === video.video_id ? 'Currently Playing' : 'Watch Now'}
                    </button>
                  )}
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      openVideoInNewTab(video.video_id);
                    }}
                    className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors flex items-center"
                  >
                    <ExternalLink className="h-4 w-4 mr-2" />
                    YouTube
                  </button>
                </div>
              </div>
            </div>
          </motion.div>
        ))}
      </div>

      {/* Disclaimer */}
      <div className="bg-amber-50 border border-amber-200 rounded-2xl p-4">
        <div className="flex items-start">
          <AlertTriangle className="h-5 w-5 text-amber-600 mr-3 mt-0.5 flex-shrink-0" />
          <div>
            <h5 className="font-semibold text-amber-800 mb-1">Educational Content Only</h5>
            <p className="text-amber-700 text-sm">
              These videos are for educational purposes only and should not replace professional medical advice. 
              Always consult qualified Ayurvedic practitioners or healthcare professionals for proper treatment.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default YouTubeVideos;