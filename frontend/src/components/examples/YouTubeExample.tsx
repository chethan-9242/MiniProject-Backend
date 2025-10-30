import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Search, Play } from 'lucide-react';
import YouTubeVideos from '../YouTubeVideos';

const YouTubeExample: React.FC = () => {
  const [searchCondition, setSearchCondition] = useState('');
  const [currentCondition, setCurrentCondition] = useState('');

  const handleSearch = () => {
    if (searchCondition.trim()) {
      setCurrentCondition(searchCondition.trim());
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  const popularConditions = [
    'Acne',
    'Eczema',
    'Hair Loss',
    'Dandruff',
    'Psoriasis',
    'Dry Skin',
    'Premature Graying'
  ];

  return (
    <div className="max-w-6xl mx-auto p-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center mb-8"
      >
        <h1 className="text-3xl font-bold text-gray-900 mb-4">
          Ayurvedic Treatment Videos
        </h1>
        <p className="text-gray-600 max-w-2xl mx-auto">
          Search for educational videos on traditional Ayurvedic remedies for various health conditions.
          Our AI-powered system finds the most relevant and credible content.
        </p>
      </motion.div>

      {/* Search Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="bg-white rounded-2xl shadow-lg p-6 mb-8"
      >
        <div className="flex flex-col md:flex-row gap-4">
          <div className="flex-1">
            <input
              type="text"
              value={searchCondition}
              onChange={(e) => setSearchCondition(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Enter a condition (e.g., acne, hair loss, eczema)..."
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-ayurveda-500 focus:border-transparent"
            />
          </div>
          <button
            onClick={handleSearch}
            disabled={!searchCondition.trim()}
            className="px-6 py-3 bg-ayurveda-600 text-white rounded-lg hover:bg-ayurveda-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center space-x-2"
          >
            <Search className="h-5 w-5" />
            <span>Search Videos</span>
          </button>
        </div>

        {/* Popular Conditions */}
        <div className="mt-4">
          <p className="text-sm text-gray-600 mb-2">Popular searches:</p>
          <div className="flex flex-wrap gap-2">
            {popularConditions.map((condition) => (
              <button
                key={condition}
                onClick={() => {
                  setSearchCondition(condition);
                  setCurrentCondition(condition);
                }}
                className="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-sm hover:bg-ayurveda-100 hover:text-ayurveda-700 transition-colors"
              >
                {condition}
              </button>
            ))}
          </div>
        </div>
      </motion.div>

      {/* YouTube Videos Results */}
      {currentCondition && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
        >
          <YouTubeVideos 
            condition={currentCondition}
            maxResults={6}
            showEmbeddedPlayer={true}
          />
        </motion.div>
      )}

      {/* No Search State */}
      {!currentCondition && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="text-center py-12"
        >
          <Play className="h-16 w-16 text-gray-400 mx-auto mb-4" />
          <h3 className="text-xl font-semibold text-gray-700 mb-2">
            Start Your Search
          </h3>
          <p className="text-gray-500">
            Enter a condition above to find relevant Ayurvedic treatment videos
          </p>
        </motion.div>
      )}

      {/* API Information */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.6 }}
        className="mt-12 bg-ayurveda-50 border border-ayurveda-200 rounded-2xl p-6"
      >
        <h3 className="text-lg font-semibold text-ayurveda-800 mb-2">
          How Our Video Search Works
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-ayurveda-700">
          <div>
            <h4 className="font-medium mb-1">Intelligent Matching</h4>
            <p>Our system searches for videos using Ayurvedic terminology and traditional treatment keywords.</p>
          </div>
          <div>
            <h4 className="font-medium mb-1">Quality Filtering</h4>
            <p>Videos are ranked by view count, engagement, and relevance to ensure high-quality content.</p>
          </div>
          <div>
            <h4 className="font-medium mb-1">Educational Focus</h4>
            <p>All content is filtered to prioritize educational and instructional videos over commercial content.</p>
          </div>
          <div>
            <h4 className="font-medium mb-1">Traditional Knowledge</h4>
            <p>Search results emphasize authentic Ayurvedic practices and traditional healing methods.</p>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default YouTubeExample;