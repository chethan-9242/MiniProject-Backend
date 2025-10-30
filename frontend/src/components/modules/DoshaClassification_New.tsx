import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Heart, ChevronRight, ChevronLeft, BarChart3, User, CheckCircle, AlertCircle } from 'lucide-react';
import axios from 'axios';

const API_URL = (process.env.REACT_APP_API_URL || 'http://localhost:8000').replace(/\/$/, '');

interface Question {
  id: string;
  question: string;
  options: {
    value: string;
    label: string;
    description: string;
  }[];
}

interface DoshaResult {
  vata: number;
  pitta: number;
  kapha: number;
  dominant_dosha: string;
  secondary_dosha: string;
  dosha_description: string;
  health_recommendations: string[];
  dietary_guidelines: string[];
  lifestyle_tips: string[];
  warning_signs: string[];
}

const DoshaClassificationNew: React.FC = () => {
  const [currentStep, setCurrentStep] = useState(0);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<DoshaResult | null>(null);

  // 10 Essential Dosha Assessment Questions
  const questions: Question[] = [
    {
      id: 'body_frame',
      question: 'How would you describe your body frame?',
      options: [
        { value: 'thin', label: 'Thin & Lean', description: 'Slender build, difficulty gaining weight' },
        { value: 'medium', label: 'Medium & Muscular', description: 'Athletic build, moderate weight' },
        { value: 'large', label: 'Large & Solid', description: 'Broad frame, easy to gain weight' }
      ]
    },
    {
      id: 'skin_type',
      question: 'What best describes your skin?',
      options: [
        { value: 'dry', label: 'Dry & Rough', description: 'Tends to be dry, needs moisturizing' },
        { value: 'sensitive', label: 'Sensitive & Warm', description: 'Sensitive, prone to rashes or acne' },
        { value: 'oily', label: 'Oily & Smooth', description: 'Well-moisturized, smooth texture' }
      ]
    },
    {
      id: 'digestion',
      question: 'How is your digestion typically?',
      options: [
        { value: 'irregular', label: 'Irregular', description: 'Variable, sometimes gas or bloating' },
        { value: 'strong', label: 'Strong & Fast', description: 'Good appetite, burns food quickly' },
        { value: 'slow', label: 'Slow & Steady', description: 'Steady, can skip meals easily' }
      ]
    },
    {
      id: 'sleep_pattern',
      question: 'How would you describe your sleep?',
      options: [
        { value: 'light', label: 'Light Sleeper', description: 'Easily disturbed, trouble falling asleep' },
        { value: 'moderate', label: 'Moderate', description: 'Sound sleep with occasional disturbances' },
        { value: 'deep', label: 'Deep Sleeper', description: 'Heavy sleep, hard to wake up' }
      ]
    },
    {
      id: 'stress_response',
      question: 'When under stress, you tend to feel:',
      options: [
        { value: 'anxious', label: 'Anxious & Worried', description: 'Nervous, worried, overwhelmed' },
        { value: 'irritable', label: 'Irritable & Angry', description: 'Short-tempered, frustrated' },
        { value: 'withdrawn', label: 'Withdrawn & Lethargic', description: 'Want to isolate, feel heavy' }
      ]
    },
    {
      id: 'climate_preference',
      question: 'Which climate do you prefer?',
      options: [
        { value: 'warm', label: 'Warm & Sunny', description: 'Prefer warmth, dislike cold' },
        { value: 'cool', label: 'Cool & Breezy', description: 'Prefer cooler temperatures' },
        { value: 'moderate_temp', label: 'Moderate', description: 'Comfortable in most climates' }
      ]
    },
    {
      id: 'energy_level',
      question: 'Your energy levels throughout the day are:',
      options: [
        { value: 'variable', label: 'Variable & Fluctuating', description: 'Bursts of energy, then fatigue' },
        { value: 'high', label: 'High & Intense', description: 'Consistent high energy' },
        { value: 'steady', label: 'Steady & Enduring', description: 'Stable, long-lasting energy' }
      ]
    },
    {
      id: 'appetite',
      question: 'Your appetite is typically:',
      options: [
        { value: 'irregular_appetite', label: 'Irregular', description: 'Sometimes hungry, sometimes not' },
        { value: 'strong_appetite', label: 'Strong & Regular', description: 'Get hungry at regular intervals' },
        { value: 'steady_appetite', label: 'Steady & Mild', description: 'Can skip meals without discomfort' }
      ]
    },
    {
      id: 'mental_state',
      question: 'Your mental state is usually:',
      options: [
        { value: 'creative', label: 'Creative & Active', description: 'Quick thinker, creative, restless mind' },
        { value: 'focused', label: 'Focused & Sharp', description: 'Analytical, decisive, goal-oriented' },
        { value: 'calm', label: 'Calm & Steady', description: 'Relaxed, methodical, slow to change' }
      ]
    },
    {
      id: 'physical_activity',
      question: 'Your preferred pace of physical activity is:',
      options: [
        { value: 'quick_movements', label: 'Quick & Varied', description: 'Fast movements, easily distracted' },
        { value: 'purposeful', label: 'Purposeful & Intense', description: 'Competitive, goal-driven exercise' },
        { value: 'slow_steady', label: 'Slow & Steady', description: 'Consistent, moderate-paced activity' }
      ]
    }
  ];

  const handleAnswer = (questionId: string, value: string) => {
    setAnswers({ ...answers, [questionId]: value });
    
    // Auto-advance to next question
    if (currentStep < questions.length - 1) {
      setTimeout(() => setCurrentStep(currentStep + 1), 300);
    }
  };

  const analyzeDosha = async () => {
    setLoading(true);
    
    try {
      const response = await axios.post(`${API_URL}/api/dosha/analyze`, answers);
      setResult(response.data);
    } catch (error) {
      console.error('Dosha analysis failed:', error);
      alert('Analysis failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const resetQuiz = () => {
    setCurrentStep(0);
    setAnswers({});
    setResult(null);
  };

  const getDoshaColor = (dosha: string) => {
    switch (dosha.toLowerCase()) {
      case 'vata': return 'from-blue-500 to-indigo-600';
      case 'pitta': return 'from-orange-500 to-red-600';
      case 'kapha': return 'from-green-500 to-teal-600';
      default: return 'from-gray-500 to-gray-600';
    }
  };

  if (result) {
    return (
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="max-w-5xl mx-auto px-4 py-8"
      >
        {/* Header */}
        <div className="text-center mb-8">
          <h2 className="text-4xl font-bold text-gray-900 mb-2">Your Dosha Profile</h2>
          <p className="text-gray-600">Based on Ayurvedic principles and AI analysis</p>
        </div>

        {/* Dosha Scores */}
        <div className="bg-white rounded-2xl shadow-lg p-8 mb-8">
          <div className="grid md:grid-cols-3 gap-6 mb-8">
            <div className="text-center">
              <div className="text-5xl font-bold text-blue-600 mb-2">{result.vata}%</div>
              <div className="text-lg font-semibold text-gray-800">Vata</div>
              <div className="text-sm text-gray-600">Air & Space</div>
            </div>
            <div className="text-center">
              <div className="text-5xl font-bold text-orange-600 mb-2">{result.pitta}%</div>
              <div className="text-lg font-semibold text-gray-800">Pitta</div>
              <div className="text-sm text-gray-600">Fire & Water</div>
            </div>
            <div className="text-center">
              <div className="text-5xl font-bold text-green-600 mb-2">{result.kapha}%</div>
              <div className="text-lg font-semibold text-gray-800">Kapha</div>
              <div className="text-sm text-gray-600">Earth & Water</div>
            </div>
          </div>

          {/* Dominant Dosha */}
          <div className={`bg-gradient-to-r ${getDoshaColor(result.dominant_dosha)} text-white rounded-xl p-6 mb-6`}>
            <h3 className="text-2xl font-bold mb-2">Your Dominant Dosha: {result.dominant_dosha}</h3>
            <p className="text-white/90">{result.dosha_description}</p>
          </div>

          {/* Visual Progress Bars */}
          <div className="space-y-4">
            <div>
              <div className="flex justify-between mb-1">
                <span className="text-sm font-medium text-blue-700">Vata</span>
                <span className="text-sm font-medium text-blue-700">{result.vata}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-3">
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: `${result.vata}%` }}
                  transition={{ duration: 1, delay: 0.2 }}
                  className="bg-blue-600 h-3 rounded-full"
                />
              </div>
            </div>
            <div>
              <div className="flex justify-between mb-1">
                <span className="text-sm font-medium text-orange-700">Pitta</span>
                <span className="text-sm font-medium text-orange-700">{result.pitta}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-3">
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: `${result.pitta}%` }}
                  transition={{ duration: 1, delay: 0.4 }}
                  className="bg-orange-600 h-3 rounded-full"
                />
              </div>
            </div>
            <div>
              <div className="flex justify-between mb-1">
                <span className="text-sm font-medium text-green-700">Kapha</span>
                <span className="text-sm font-medium text-green-700">{result.kapha}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-3">
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: `${result.kapha}%` }}
                  transition={{ duration: 1, delay: 0.6 }}
                  className="bg-green-600 h-3 rounded-full"
                />
              </div>
            </div>
          </div>
        </div>

        {/* Recommendations Grid */}
        <div className="grid md:grid-cols-2 gap-6 mb-8">
          {/* Health Recommendations */}
          <div className="bg-white rounded-2xl shadow-lg p-6">
            <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
              <Heart className="h-6 w-6 text-red-500 mr-2" />
              Health Recommendations
            </h3>
            <ul className="space-y-3">
              {result.health_recommendations.map((rec, index) => (
                <li key={index} className="flex items-start">
                  <CheckCircle className="h-5 w-5 text-green-500 mr-2 mt-0.5 flex-shrink-0" />
                  <span className="text-gray-700">{rec}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Dietary Guidelines */}
          <div className="bg-white rounded-2xl shadow-lg p-6">
            <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
              <svg className="h-6 w-6 text-orange-500 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
              Dietary Guidelines
            </h3>
            <ul className="space-y-3">
              {result.dietary_guidelines.map((guide, index) => (
                <li key={index} className="flex items-start">
                  <CheckCircle className="h-5 w-5 text-green-500 mr-2 mt-0.5 flex-shrink-0" />
                  <span className="text-gray-700">{guide}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Lifestyle Tips */}
          <div className="bg-white rounded-2xl shadow-lg p-6">
            <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
              <User className="h-6 w-6 text-blue-500 mr-2" />
              Lifestyle Tips
            </h3>
            <ul className="space-y-3">
              {result.lifestyle_tips.map((tip, index) => (
                <li key={index} className="flex items-start">
                  <CheckCircle className="h-5 w-5 text-green-500 mr-2 mt-0.5 flex-shrink-0" />
                  <span className="text-gray-700">{tip}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Warning Signs */}
          <div className="bg-white rounded-2xl shadow-lg p-6">
            <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
              <AlertCircle className="h-6 w-6 text-amber-500 mr-2" />
              Warning Signs
            </h3>
            <ul className="space-y-3">
              {result.warning_signs.map((sign, index) => (
                <li key={index} className="flex items-start">
                  <AlertCircle className="h-5 w-5 text-amber-500 mr-2 mt-0.5 flex-shrink-0" />
                  <span className="text-gray-700">{sign}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Action Button */}
        <div className="text-center">
          <button
            onClick={resetQuiz}
            className="px-8 py-4 bg-ayurveda-600 text-white font-semibold rounded-full hover:bg-ayurveda-700 transition-colors shadow-lg"
          >
            Take Assessment Again
          </button>
        </div>
      </motion.div>
    );
  }

  const currentQuestion = questions[currentStep];
  const progress = ((currentStep + 1) / questions.length) * 100;
  const isComplete = Object.keys(answers).length === questions.length;

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="max-w-3xl mx-auto px-4 py-8"
    >
      {/* Header */}
      <div className="text-center mb-8">
        <Heart className="h-16 w-16 text-ayurveda-600 mx-auto mb-4" />
        <h1 className="text-4xl font-bold text-gray-900 mb-2">Dosha Assessment</h1>
        <p className="text-lg text-gray-600">10 Questions · Powered by AI</p>
      </div>

      {/* Progress Bar */}
      <div className="mb-8">
        <div className="flex justify-between text-sm text-gray-600 mb-2">
          <span>Question {currentStep + 1} of {questions.length}</span>
          <span>{Math.round(progress)}% Complete</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <motion.div
            initial={{ width: 0 }}
            animate={{ width: `${progress}%` }}
            className="bg-ayurveda-600 h-2 rounded-full transition-all duration-300"
          />
        </div>
      </div>

      {/* Question Card */}
      <AnimatePresence mode="wait">
        <motion.div
          key={currentStep}
          initial={{ opacity: 0, x: 50 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: -50 }}
          className="bg-white rounded-2xl shadow-xl p-8 mb-6"
        >
          <h2 className="text-2xl font-bold text-gray-900 mb-6">{currentQuestion.question}</h2>
          
          <div className="space-y-4">
            {currentQuestion.options.map((option) => (
              <button
                key={option.value}
                onClick={() => handleAnswer(currentQuestion.id, option.value)}
                className={`w-full p-6 rounded-xl text-left transition-all border-2 ${
                  answers[currentQuestion.id] === option.value
                    ? 'border-ayurveda-600 bg-ayurveda-50'
                    : 'border-gray-200 hover:border-ayurveda-300 hover:bg-gray-50'
                }`}
              >
                <div className="flex items-start">
                  <div className={`w-6 h-6 rounded-full border-2 mr-4 mt-1 flex items-center justify-center flex-shrink-0 ${
                    answers[currentQuestion.id] === option.value
                      ? 'border-ayurveda-600 bg-ayurveda-600'
                      : 'border-gray-300'
                  }`}>
                    {answers[currentQuestion.id] === option.value && (
                      <CheckCircle className="h-4 w-4 text-white" />
                    )}
                  </div>
                  <div className="flex-1">
                    <div className="font-semibold text-gray-900 mb-1">{option.label}</div>
                    <div className="text-sm text-gray-600">{option.description}</div>
                  </div>
                </div>
              </button>
            ))}
          </div>
        </motion.div>
      </AnimatePresence>

      {/* Navigation */}
      <div className="flex justify-between items-center">
        <button
          onClick={() => setCurrentStep(Math.max(0, currentStep - 1))}
          disabled={currentStep === 0}
          className="flex items-center px-6 py-3 text-gray-700 font-medium rounded-full border border-gray-300 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          <ChevronLeft className="h-5 w-5 mr-2" />
          Previous
        </button>

        {isComplete ? (
          <button
            onClick={analyzeDosha}
            disabled={loading}
            className="flex items-center px-8 py-4 bg-ayurveda-600 text-white font-semibold rounded-full hover:bg-ayurveda-700 disabled:opacity-50 transition-colors shadow-lg"
          >
            {loading ? (
              <>
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2" />
                Analyzing...
              </>
            ) : (
              <>
                <BarChart3 className="h-5 w-5 mr-2" />
                Get Results
              </>
            )}
          </button>
        ) : (
          <button
            onClick={() => setCurrentStep(Math.min(questions.length - 1, currentStep + 1))}
            disabled={!answers[currentQuestion.id]}
            className="flex items-center px-6 py-3 bg-ayurveda-600 text-white font-medium rounded-full hover:bg-ayurveda-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            Next
            <ChevronRight className="h-5 w-5 ml-2" />
          </button>
        )}
      </div>
    </motion.div>
  );
};

export default DoshaClassificationNew;
