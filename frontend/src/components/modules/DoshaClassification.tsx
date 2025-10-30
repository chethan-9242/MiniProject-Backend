import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Heart, ChevronRight, ChevronLeft, BarChart3, User } from 'lucide-react';
import axios from 'axios';

interface Question {
  id: string;
  category: string;
  question: string;
  options: {
    value: string;
    label: string;
    dosha: 'vata' | 'pitta' | 'kapha';
  }[];
}

interface DoshaResult {
  vata: number;
  pitta: number;
  kapha: number;
  dominant_dosha: string;
  recommendations: string[];
}

const DoshaClassification: React.FC = () => {
  const [currentStep, setCurrentStep] = useState(0);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<DoshaResult | null>(null);

  // 43 comprehensive assessment questions based on traditional Ayurvedic parameters
  const questions: Question[] = [
    // Physical Constitution (10 questions)
    {
      id: 'body_frame',
      category: 'Physical Constitution',
      question: 'How would you describe your body frame?',
      options: [
        { value: 'thin', label: 'Thin, lean build', dosha: 'vata' },
        { value: 'medium', label: 'Medium, muscular build', dosha: 'pitta' },
        { value: 'large', label: 'Large, broad build', dosha: 'kapha' }
      ]
    },
    {
      id: 'weight',
      category: 'Physical Constitution',
      question: 'Your weight tends to be:',
      options: [
        { value: 'low', label: 'Below average, hard to gain', dosha: 'vata' },
        { value: 'medium', label: 'Average, fluctuates', dosha: 'pitta' },
        { value: 'high', label: 'Above average, easy to gain', dosha: 'kapha' }
      ]
    },
    {
      id: 'skin_type',
      category: 'Physical Constitution',
      question: 'Your skin is generally:',
      options: [
        { value: 'dry', label: 'Dry, rough, thin', dosha: 'vata' },
        { value: 'oily', label: 'Oily, warm, sensitive', dosha: 'pitta' },
        { value: 'thick', label: 'Thick, smooth, oily', dosha: 'kapha' }
      ]
    },
    {
      id: 'hair_type',
      category: 'Physical Constitution',
      question: 'Your hair is typically:',
      options: [
        { value: 'dry', label: 'Dry, brittle, kinky', dosha: 'vata' },
        { value: 'fine', label: 'Fine, oily, early graying', dosha: 'pitta' },
        { value: 'thick', label: 'Thick, lustrous, wavy', dosha: 'kapha' }
      ]
    },
    {
      id: 'eyes',
      category: 'Physical Constitution',
      question: 'Your eyes are:',
      options: [
        { value: 'small', label: 'Small, active, dry', dosha: 'vata' },
        { value: 'penetrating', label: 'Penetrating, bright, sensitive', dosha: 'pitta' },
        { value: 'large', label: 'Large, calm, attractive', dosha: 'kapha' }
      ]
    },
    {
      id: 'nails',
      category: 'Physical Constitution',
      question: 'Your nails are:',
      options: [
        { value: 'brittle', label: 'Brittle, break easily', dosha: 'vata' },
        { value: 'soft', label: 'Soft, pink, flexible', dosha: 'pitta' },
        { value: 'strong', label: 'Strong, thick, smooth', dosha: 'kapha' }
      ]
    },
    {
      id: 'lips',
      category: 'Physical Constitution',
      question: 'Your lips are:',
      options: [
        { value: 'dry', label: 'Dry, often chapped', dosha: 'vata' },
        { value: 'soft', label: 'Soft, medium size', dosha: 'pitta' },
        { value: 'smooth', label: 'Smooth, large, attractive', dosha: 'kapha' }
      ]
    },
    {
      id: 'teeth',
      category: 'Physical Constitution',
      question: 'Your teeth are:',
      options: [
        { value: 'irregular', label: 'Irregular, protruding', dosha: 'vata' },
        { value: 'medium', label: 'Medium size, yellowish', dosha: 'pitta' },
        { value: 'large', label: 'Large, white, strong', dosha: 'kapha' }
      ]
    },
    {
      id: 'joints',
      category: 'Physical Constitution',
      question: 'Your joints are:',
      options: [
        { value: 'prominent', label: 'Prominent, crack easily', dosha: 'vata' },
        { value: 'loose', label: 'Loose, flexible', dosha: 'pitta' },
        { value: 'large', label: 'Large, well-formed', dosha: 'kapha' }
      ]
    },
    {
      id: 'veins',
      category: 'Physical Constitution',
      question: 'Your veins and tendons are:',
      options: [
        { value: 'prominent', label: 'Prominent, visible', dosha: 'vata' },
        { value: 'moderately', label: 'Moderately visible', dosha: 'pitta' },
        { value: 'well_covered', label: 'Well covered, not visible', dosha: 'kapha' }
      ]
    },
    
    // Digestion & Metabolism (8 questions)
    {
      id: 'appetite',
      category: 'Digestion & Metabolism',
      question: 'Your appetite is:',
      options: [
        { value: 'irregular', label: 'Irregular, varies greatly', dosha: 'vata' },
        { value: 'strong', label: 'Strong, can eat large meals', dosha: 'pitta' },
        { value: 'steady', label: 'Steady, can skip meals', dosha: 'kapha' }
      ]
    },
    {
      id: 'thirst',
      category: 'Digestion & Metabolism',
      question: 'Your thirst is:',
      options: [
        { value: 'variable', label: 'Variable, inconsistent', dosha: 'vata' },
        { value: 'excessive', label: 'Excessive, need cold drinks', dosha: 'pitta' },
        { value: 'minimal', label: 'Minimal, satisfied easily', dosha: 'kapha' }
      ]
    },
    {
      id: 'food_preference',
      category: 'Digestion & Metabolism',
      question: 'You prefer foods that are:',
      options: [
        { value: 'warm', label: 'Warm, oily, heavy', dosha: 'vata' },
        { value: 'cool', label: 'Cool, sweet, mild', dosha: 'pitta' },
        { value: 'spicy', label: 'Spicy, bitter, hot', dosha: 'kapha' }
      ]
    },
    {
      id: 'digestion_speed',
      category: 'Digestion & Metabolism',
      question: 'Your digestion is:',
      options: [
        { value: 'irregular', label: 'Irregular, sometimes gas/bloating', dosha: 'vata' },
        { value: 'strong', label: 'Strong, quick, acidic', dosha: 'pitta' },
        { value: 'slow', label: 'Slow, steady, heavy feeling', dosha: 'kapha' }
      ]
    },
    {
      id: 'bowel_movements',
      category: 'Digestion & Metabolism',
      question: 'Your bowel movements are:',
      options: [
        { value: 'irregular', label: 'Irregular, dry, constipated', dosha: 'vata' },
        { value: 'regular', label: 'Regular, loose, frequent', dosha: 'pitta' },
        { value: 'slow', label: 'Slow, heavy, regular', dosha: 'kapha' }
      ]
    },
    {
      id: 'metabolism',
      category: 'Digestion & Metabolism',
      question: 'Your metabolism is:',
      options: [
        { value: 'irregular', label: 'Irregular, sometimes high/low', dosha: 'vata' },
        { value: 'fast', label: 'Fast, burn calories quickly', dosha: 'pitta' },
        { value: 'slow', label: 'Slow, gain weight easily', dosha: 'kapha' }
      ]
    },
    {
      id: 'eating_speed',
      category: 'Digestion & Metabolism',
      question: 'You eat:',
      options: [
        { value: 'quickly', label: 'Quickly, irregularly', dosha: 'vata' },
        { value: 'moderately', label: 'Moderately fast, regularly', dosha: 'pitta' },
        { value: 'slowly', label: 'Slowly, enjoy food', dosha: 'kapha' }
      ]
    },
    {
      id: 'taste_preference',
      category: 'Digestion & Metabolism',
      question: 'You crave tastes that are:',
      options: [
        { value: 'sweet', label: 'Sweet, sour, salty', dosha: 'vata' },
        { value: 'sweet_bitter', label: 'Sweet, bitter, astringent', dosha: 'pitta' },
        { value: 'pungent', label: 'Pungent, bitter, astringent', dosha: 'kapha' }
      ]
    },

    // Sleep Patterns (5 questions)
    {
      id: 'sleep_quality',
      category: 'Sleep Patterns',
      question: 'Your sleep is:',
      options: [
        { value: 'light', label: 'Light, interrupted, restless', dosha: 'vata' },
        { value: 'moderate', label: 'Moderate, may have vivid dreams', dosha: 'pitta' },
        { value: 'deep', label: 'Deep, prolonged, difficult to wake', dosha: 'kapha' }
      ]
    },
    {
      id: 'sleep_duration',
      category: 'Sleep Patterns',
      question: 'You need:',
      options: [
        { value: 'less', label: 'Less sleep, 5-7 hours', dosha: 'vata' },
        { value: 'moderate', label: 'Moderate sleep, 6-8 hours', dosha: 'pitta' },
        { value: 'more', label: 'More sleep, 8+ hours', dosha: 'kapha' }
      ]
    },
    {
      id: 'falling_asleep',
      category: 'Sleep Patterns',
      question: 'Falling asleep is:',
      options: [
        { value: 'difficult', label: 'Difficult, mind races', dosha: 'vata' },
        { value: 'variable', label: 'Variable, depends on day', dosha: 'pitta' },
        { value: 'easy', label: 'Easy, fall asleep quickly', dosha: 'kapha' }
      ]
    },
    {
      id: 'dreams',
      category: 'Sleep Patterns',
      question: 'Your dreams are:',
      options: [
        { value: 'active', label: 'Active, fearful, flying', dosha: 'vata' },
        { value: 'vivid', label: 'Vivid, colorful, intense', dosha: 'pitta' },
        { value: 'peaceful', label: 'Peaceful, romantic, watery', dosha: 'kapha' }
      ]
    },
    {
      id: 'wake_up',
      category: 'Sleep Patterns',
      question: 'Waking up is:',
      options: [
        { value: 'easy', label: 'Easy, alert quickly', dosha: 'vata' },
        { value: 'moderate', label: 'Moderate, depends on sleep quality', dosha: 'pitta' },
        { value: 'difficult', label: 'Difficult, need time to get going', dosha: 'kapha' }
      ]
    },

    // Mental & Emotional (10 questions)
    {
      id: 'mind_activity',
      category: 'Mental & Emotional',
      question: 'Your mind is:',
      options: [
        { value: 'active', label: 'Very active, restless', dosha: 'vata' },
        { value: 'sharp', label: 'Sharp, penetrating, focused', dosha: 'pitta' },
        { value: 'calm', label: 'Calm, steady, slow', dosha: 'kapha' }
      ]
    },
    {
      id: 'memory',
      category: 'Mental & Emotional',
      question: 'Your memory is:',
      options: [
        { value: 'quick_forget', label: 'Quick to learn, quick to forget', dosha: 'vata' },
        { value: 'sharp', label: 'Sharp, clear, precise', dosha: 'pitta' },
        { value: 'slow_retain', label: 'Slow to learn, good retention', dosha: 'kapha' }
      ]
    },
    {
      id: 'concentration',
      category: 'Mental & Emotional',
      question: 'Your concentration is:',
      options: [
        { value: 'short', label: 'Short-term, easily distracted', dosha: 'vata' },
        { value: 'good', label: 'Good when interested', dosha: 'pitta' },
        { value: 'prolonged', label: 'Prolonged, steady focus', dosha: 'kapha' }
      ]
    },
    {
      id: 'decision_making',
      category: 'Mental & Emotional',
      question: 'You make decisions:',
      options: [
        { value: 'quickly_change', label: 'Quickly, but change mind often', dosha: 'vata' },
        { value: 'reasonably_quick', label: 'Reasonably quick, stick to them', dosha: 'pitta' },
        { value: 'slowly_deliberate', label: 'Slowly, after much deliberation', dosha: 'kapha' }
      ]
    },
    {
      id: 'emotional_nature',
      category: 'Mental & Emotional',
      question: 'Emotionally, you are:',
      options: [
        { value: 'changeable', label: 'Changeable, moody', dosha: 'vata' },
        { value: 'intense', label: 'Intense, passionate', dosha: 'pitta' },
        { value: 'steady', label: 'Steady, consistent', dosha: 'kapha' }
      ]
    },
    {
      id: 'stress_response',
      category: 'Mental & Emotional',
      question: 'Under stress, you become:',
      options: [
        { value: 'anxious', label: 'Anxious, worried, fearful', dosha: 'vata' },
        { value: 'irritable', label: 'Irritable, angry, critical', dosha: 'pitta' },
        { value: 'withdrawn', label: 'Withdrawn, reclusive', dosha: 'kapha' }
      ]
    },
    {
      id: 'energy_level',
      category: 'Mental & Emotional',
      question: 'Your energy is:',
      options: [
        { value: 'variable', label: 'Variable, comes in bursts', dosha: 'vata' },
        { value: 'moderate', label: 'Moderate, can push when needed', dosha: 'pitta' },
        { value: 'steady', label: 'Steady, good endurance', dosha: 'kapha' }
      ]
    },
    {
      id: 'speech_pattern',
      category: 'Mental & Emotional',
      question: 'Your speech is:',
      options: [
        { value: 'fast', label: 'Fast, rambling, varied topics', dosha: 'vata' },
        { value: 'sharp', label: 'Sharp, precise, convincing', dosha: 'pitta' },
        { value: 'slow', label: 'Slow, melodious, measured', dosha: 'kapha' }
      ]
    },
    {
      id: 'social_nature',
      category: 'Mental & Emotional',
      question: 'Socially, you are:',
      options: [
        { value: 'outgoing_variable', label: 'Outgoing but variable', dosha: 'vata' },
        { value: 'outgoing_leader', label: 'Outgoing, natural leader', dosha: 'pitta' },
        { value: 'steady_loyal', label: 'Steady, loyal friend', dosha: 'kapha' }
      ]
    },
    {
      id: 'learning_style',
      category: 'Mental & Emotional',
      question: 'You learn best through:',
      options: [
        { value: 'hearing', label: 'Hearing, auditory learning', dosha: 'vata' },
        { value: 'seeing', label: 'Seeing, visual learning', dosha: 'pitta' },
        { value: 'doing', label: 'Doing, hands-on learning', dosha: 'kapha' }
      ]
    },

    // Physical Activity & Climate (5 questions)
    {
      id: 'activity_level',
      category: 'Physical Activity & Climate',
      question: 'Your activity level is:',
      options: [
        { value: 'high_variable', label: 'High but variable', dosha: 'vata' },
        { value: 'moderate_intense', label: 'Moderate to intense', dosha: 'pitta' },
        { value: 'low_steady', label: 'Low, steady pace', dosha: 'kapha' }
      ]
    },
    {
      id: 'exercise_preference',
      category: 'Physical Activity & Climate',
      question: 'You prefer exercise that is:',
      options: [
        { value: 'light_flexible', label: 'Light, flexible, yoga', dosha: 'vata' },
        { value: 'moderate_competitive', label: 'Moderate, competitive sports', dosha: 'pitta' },
        { value: 'heavy_endurance', label: 'Heavy, endurance activities', dosha: 'kapha' }
      ]
    },
    {
      id: 'weather_preference',
      category: 'Physical Activity & Climate',
      question: 'You prefer weather that is:',
      options: [
        { value: 'warm_humid', label: 'Warm and humid', dosha: 'vata' },
        { value: 'cool_moderate', label: 'Cool with moderate humidity', dosha: 'pitta' },
        { value: 'warm_dry', label: 'Warm and dry', dosha: 'kapha' }
      ]
    },
    {
      id: 'temperature_tolerance',
      category: 'Physical Activity & Climate',
      question: 'You tolerate:',
      options: [
        { value: 'cold_poorly', label: 'Cold poorly, prefer warmth', dosha: 'vata' },
        { value: 'heat_poorly', label: 'Heat poorly, prefer cool', dosha: 'pitta' },
        { value: 'cold_humidity_poorly', label: 'Cold and humidity poorly', dosha: 'kapha' }
      ]
    },
    {
      id: 'sweating',
      category: 'Physical Activity & Climate',
      question: 'You sweat:',
      options: [
        { value: 'little', label: 'Very little', dosha: 'vata' },
        { value: 'profusely', label: 'Profusely, with strong odor', dosha: 'pitta' },
        { value: 'moderately', label: 'Moderately, with pleasant odor', dosha: 'kapha' }
      ]
    },

    // Lifestyle & Habits (5 questions)
    {
      id: 'routine_preference',
      category: 'Lifestyle & Habits',
      question: 'You prefer:',
      options: [
        { value: 'variety', label: 'Variety, spontaneity', dosha: 'vata' },
        { value: 'moderate_routine', label: 'Moderate routine with some variety', dosha: 'pitta' },
        { value: 'regular_routine', label: 'Regular, predictable routine', dosha: 'kapha' }
      ]
    },
    {
      id: 'financial_habits',
      category: 'Lifestyle & Habits',
      question: 'With money, you are:',
      options: [
        { value: 'impulsive', label: 'Impulsive, spend on whims', dosha: 'vata' },
        { value: 'planned', label: 'Planned spender on useful items', dosha: 'pitta' },
        { value: 'saving', label: 'Good at saving, accumulating', dosha: 'kapha' }
      ]
    },
    {
      id: 'work_style',
      category: 'Lifestyle & Habits',
      question: 'Your work style is:',
      options: [
        { value: 'creative_scattered', label: 'Creative but sometimes scattered', dosha: 'vata' },
        { value: 'precise_goal_oriented', label: 'Precise and goal-oriented', dosha: 'pitta' },
        { value: 'methodical_persistent', label: 'Methodical and persistent', dosha: 'kapha' }
      ]
    },
    {
      id: 'relationships',
      category: 'Lifestyle & Habits',
      question: 'In relationships, you are:',
      options: [
        { value: 'enthusiastic_changeable', label: 'Enthusiastic but changeable', dosha: 'vata' },
        { value: 'passionate_intense', label: 'Passionate and intense', dosha: 'pitta' },
        { value: 'devoted_steady', label: 'Devoted and steady', dosha: 'kapha' }
      ]
    },
    {
      id: 'travel_preference',
      category: 'Lifestyle & Habits',
      question: 'You prefer to travel:',
      options: [
        { value: 'frequently_spontaneous', label: 'Frequently, spontaneous trips', dosha: 'vata' },
        { value: 'planned_purposeful', label: 'Planned, purposeful trips', dosha: 'pitta' },
        { value: 'occasionally_comfort', label: 'Occasionally, prefer comfort', dosha: 'kapha' }
      ]
    }
  ];

  const categories = Array.from(new Set(questions.map(q => q.category)));
  const totalSteps = categories.length;

  const handleAnswer = (questionId: string, value: string) => {
    setAnswers(prev => ({ ...prev, [questionId]: value }));
  };

  const nextStep = () => {
    if (currentStep < totalSteps - 1) {
      setCurrentStep(prev => prev + 1);
    }
  };

  const prevStep = () => {
    if (currentStep > 0) {
      setCurrentStep(prev => prev - 1);
    }
  };

  const submitAssessment = async () => {
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/api/dosha/classify', {
        answers: answers
      });
      setResult(response.data);
    } catch (error) {
      console.error('Error submitting assessment:', error);
      // Mock result for demo purposes
      const mockResult: DoshaResult = {
        vata: 35,
        pitta: 40,
        kapha: 25,
        dominant_dosha: 'Pitta',
        recommendations: [
          'Follow a cooling diet with sweet, bitter, and astringent tastes',
          'Practice calming activities like meditation and gentle yoga',
          'Avoid excessive heat and spicy foods',
          'Maintain regular meal times and sleep schedule',
          'Stay hydrated with cool (not ice-cold) water'
        ]
      };
      setResult(mockResult);
    }
    setLoading(false);
  };

  const resetAssessment = () => {
    setCurrentStep(0);
    setAnswers({});
    setResult(null);
  };

  const currentCategoryQuestions = questions.filter(q => q.category === categories[currentStep]);
  const isStepComplete = currentCategoryQuestions.every(q => answers[q.id]);

  if (result) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-4xl mx-auto"
      >
        <div className="text-center mb-8">
          <Heart className="h-16 w-16 text-ayurveda-600 mx-auto mb-4" />
          <h1 className="text-4xl font-bold text-gray-900 font-serif mb-2">
            Your Dosha Analysis Results
          </h1>
          <p className="text-lg text-gray-600">
            Based on 43 comprehensive Ayurvedic parameters
          </p>
        </div>

        {/* Dosha Percentages */}
        <div className="grid md:grid-cols-3 gap-6 mb-8">
          <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-2xl p-6 text-center">
            <h3 className="text-xl font-semibold text-blue-800 mb-2">Vata (Air)</h3>
            <div className="text-3xl font-bold text-blue-600 mb-2">{result.vata}%</div>
            <div className="w-full bg-blue-200 rounded-full h-2">
              <div 
                className="bg-blue-500 h-2 rounded-full transition-all duration-1000"
                style={{ width: `${result.vata}%` }}
              />
            </div>
          </div>
          
          <div className="bg-gradient-to-br from-red-50 to-red-100 rounded-2xl p-6 text-center">
            <h3 className="text-xl font-semibold text-red-800 mb-2">Pitta (Fire)</h3>
            <div className="text-3xl font-bold text-red-600 mb-2">{result.pitta}%</div>
            <div className="w-full bg-red-200 rounded-full h-2">
              <div 
                className="bg-red-500 h-2 rounded-full transition-all duration-1000"
                style={{ width: `${result.pitta}%` }}
              />
            </div>
          </div>
          
          <div className="bg-gradient-to-br from-green-50 to-green-100 rounded-2xl p-6 text-center">
            <h3 className="text-xl font-semibold text-green-800 mb-2">Kapha (Earth)</h3>
            <div className="text-3xl font-bold text-green-600 mb-2">{result.kapha}%</div>
            <div className="w-full bg-green-200 rounded-full h-2">
              <div 
                className="bg-green-500 h-2 rounded-full transition-all duration-1000"
                style={{ width: `${result.kapha}%` }}
              />
            </div>
          </div>
        </div>

        {/* Dominant Dosha */}
        <div className="bg-white rounded-2xl p-8 shadow-lg mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-4 flex items-center">
            <BarChart3 className="h-8 w-8 text-ayurveda-600 mr-3" />
            Your Dominant Dosha: {result.dominant_dosha}
          </h2>
          <div className="bg-ayurveda-50 rounded-lg p-6">
            <h3 className="text-lg font-semibold text-ayurveda-800 mb-3">
              Personalized Recommendations:
            </h3>
            <ul className="space-y-2">
              {result.recommendations.map((rec, index) => (
                <li key={index} className="flex items-start">
                  <span className="text-ayurveda-600 mr-2">•</span>
                  <span className="text-gray-700">{rec}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <button
            onClick={resetAssessment}
            className="px-6 py-3 bg-ayurveda-600 text-white font-semibold rounded-full hover:bg-ayurveda-700 transition-colors"
          >
            Take Assessment Again
          </button>
          <button className="px-6 py-3 border-2 border-ayurveda-600 text-ayurveda-600 font-semibold rounded-full hover:bg-ayurveda-50 transition-colors">
            Download Results
          </button>
        </div>
      </motion.div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="max-w-4xl mx-auto"
    >
      {/* Header */}
      <div className="text-center mb-8">
        <Heart className="h-16 w-16 text-ayurveda-600 mx-auto mb-4" />
        <h1 className="text-4xl font-bold text-gray-900 font-serif mb-2">
          Dosha Classification Assessment
        </h1>
        <p className="text-lg text-gray-600 mb-4">
          Comprehensive 43-parameter analysis to determine your Ayurvedic constitution
        </p>
        
        {/* Progress Bar */}
        <div className="max-w-md mx-auto">
          <div className="flex justify-between text-sm text-gray-600 mb-2">
            <span>Step {currentStep + 1} of {totalSteps}</span>
            <span>{Math.round(((currentStep + 1) / totalSteps) * 100)}% Complete</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div 
              className="bg-ayurveda-500 h-2 rounded-full transition-all duration-300"
              style={{ width: `${((currentStep + 1) / totalSteps) * 100}%` }}
            />
          </div>
        </div>
      </div>

      {/* Question Section */}
      <div className="bg-white rounded-2xl p-8 shadow-lg mb-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">
          {categories[currentStep]}
        </h2>
        
        <div className="space-y-6">
          {currentCategoryQuestions.map((question, index) => (
            <div key={question.id} className="border-b border-gray-200 pb-6 last:border-b-0">
              <h3 className="text-lg font-semibold text-gray-800 mb-4">
                {index + 1}. {question.question}
              </h3>
              <div className="space-y-2">
                {question.options.map((option) => (
                  <label
                    key={option.value}
                    className={`flex items-center p-3 rounded-lg cursor-pointer transition-colors ${
                      answers[question.id] === option.value
                        ? 'bg-ayurveda-100 border-2 border-ayurveda-500'
                        : 'bg-gray-50 border-2 border-transparent hover:bg-gray-100'
                    }`}
                  >
                    <input
                      type="radio"
                      name={question.id}
                      value={option.value}
                      checked={answers[question.id] === option.value}
                      onChange={() => handleAnswer(question.id, option.value)}
                      className="sr-only"
                    />
                    <div className={`w-4 h-4 rounded-full border-2 mr-3 ${
                      answers[question.id] === option.value
                        ? 'border-ayurveda-500 bg-ayurveda-500'
                        : 'border-gray-300'
                    }`}>
                      {answers[question.id] === option.value && (
                        <div className="w-2 h-2 bg-white rounded-full mx-auto mt-0.5" />
                      )}
                    </div>
                    <span className="text-gray-700">{option.label}</span>
                  </label>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Navigation */}
      <div className="flex justify-between items-center">
        <button
          onClick={prevStep}
          disabled={currentStep === 0}
          className={`flex items-center px-6 py-3 rounded-full font-semibold transition-colors ${
            currentStep === 0
              ? 'bg-gray-200 text-gray-400 cursor-not-allowed'
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          }`}
        >
          <ChevronLeft className="h-5 w-5 mr-2" />
          Previous
        </button>

        {currentStep === totalSteps - 1 ? (
          <button
            onClick={submitAssessment}
            disabled={!isStepComplete || loading}
            className={`flex items-center px-8 py-3 rounded-full font-semibold transition-colors ${
              isStepComplete && !loading
                ? 'bg-ayurveda-600 text-white hover:bg-ayurveda-700'
                : 'bg-gray-300 text-gray-500 cursor-not-allowed'
            }`}
          >
            {loading ? (
              <>
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2" />
                Analyzing...
              </>
            ) : (
              <>
                Get Results
                <User className="h-5 w-5 ml-2" />
              </>
            )}
          </button>
        ) : (
          <button
            onClick={nextStep}
            disabled={!isStepComplete}
            className={`flex items-center px-6 py-3 rounded-full font-semibold transition-colors ${
              isStepComplete
                ? 'bg-ayurveda-600 text-white hover:bg-ayurveda-700'
                : 'bg-gray-300 text-gray-500 cursor-not-allowed'
            }`}
          >
            Next
            <ChevronRight className="h-5 w-5 ml-2" />
          </button>
        )}
      </div>
    </motion.div>
  );
};

export default DoshaClassification;