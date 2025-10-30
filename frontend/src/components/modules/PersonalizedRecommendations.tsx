import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Sparkles, Utensils, Activity, Moon, Leaf } from 'lucide-react';

interface Recommendations {
  diet: {
    foods_to_include: string[];
    foods_to_avoid: string[];
    meal_timing: string;
    cooking_tips: string[];
  };
  yoga: {
    recommended_poses: Array<{
      name: string;
      benefits: string;
      duration: string;
    }>;
    breathing_exercises: string[];
    meditation_type: string;
  };
  lifestyle: {
    daily_routine: string[];
    sleep_recommendations: string[];
    exercise_guidelines: string[];
  };
  herbal_remedies: Array<{
    herb: string;
    benefits: string;
    usage: string;
    caution?: string;
  }>;
}

const PersonalizedRecommendations: React.FC = () => {
  const [loading, setLoading] = useState(true);
  const [recommendations, setRecommendations] = useState<Recommendations | null>(null);
  const [activeTab, setActiveTab] = useState<'diet' | 'yoga' | 'lifestyle' | 'herbs'>('diet');

  useEffect(() => {
    // Simulate loading and API call
    setTimeout(() => {
      const mockRecommendations: Recommendations = {
        diet: {
          foods_to_include: [
            'Warm, cooked foods (soups, stews, casseroles)',
            'Sweet fruits (bananas, dates, figs, grapes)',
            'Whole grains (rice, wheat, oats)',
            'Healthy fats (ghee, olive oil, avocado)',
            'Warm spices (ginger, cinnamon, cardamom)',
            'Dairy products (warm milk, yogurt)',
            'Nuts and seeds (almonds, sesame seeds)',
            'Root vegetables (sweet potato, carrots, beets)'
          ],
          foods_to_avoid: [
            'Cold, raw foods and drinks',
            'Excessive spicy, bitter, or astringent foods',
            'Processed and packaged foods',
            'Caffeine and alcohol in excess',
            'Irregular eating patterns',
            'Eating while distracted or stressed',
            'Very light meals or skipping meals',
            'Ice-cold beverages with meals'
          ],
          meal_timing: 'Eat your largest meal at midday (12-1 PM) when digestive fire is strongest. Have breakfast between 7-9 AM and light dinner before 7 PM.',
          cooking_tips: [
            'Use warming spices like ginger, cumin, and black pepper',
            'Cook with ghee or sesame oil',
            'Prefer steaming, sautéing, and slow cooking methods',
            'Add a pinch of rock salt to enhance digestion'
          ]
        },
        yoga: {
          recommended_poses: [
            {
              name: 'Sun Salutations (Surya Namaskara)',
              benefits: 'Builds heat, improves circulation, energizes the body',
              duration: '5-10 minutes'
            },
            {
              name: 'Warrior Poses (Virabhadrasana)',
              benefits: 'Strengthens legs, improves balance and confidence',
              duration: '2-3 minutes each side'
            },
            {
              name: 'Tree Pose (Vrikshasana)',
              benefits: 'Improves balance, calms the mind, strengthens legs',
              duration: '1-2 minutes each side'
            },
            {
              name: 'Child\'s Pose (Balasana)',
              benefits: 'Reduces stress, calms the nervous system',
              duration: '3-5 minutes'
            },
            {
              name: 'Legs Up the Wall (Viparita Karani)',
              benefits: 'Improves circulation, reduces anxiety',
              duration: '5-10 minutes'
            }
          ],
          breathing_exercises: [
            'Nadi Shodhana (Alternate Nostril Breathing) - 5-10 minutes',
            'Ujjayi Pranayama (Ocean Breath) - during yoga practice',
            'Bhramari Pranayama (Humming Bee Breath) - for calming'
          ],
          meditation_type: 'Guided meditation or mantra meditation for 10-20 minutes daily, preferably in the morning'
        },
        lifestyle: {
          daily_routine: [
            'Wake up between 5:30-6:30 AM',
            'Start with warm water and lemon',
            'Practice oil pulling (5-10 minutes)',
            'Morning meditation and pranayama (15-20 minutes)',
            'Gentle yoga or exercise (20-30 minutes)',
            'Warm shower followed by self-massage with sesame oil',
            'Eat meals at consistent times',
            'Take short walks after meals',
            'Evening relaxation practices',
            'Sleep by 10-10:30 PM'
          ],
          sleep_recommendations: [
            'Create a calm bedtime routine starting 1 hour before sleep',
            'Avoid screens and stimulating activities before bed',
            'Practice gentle stretches or restorative yoga',
            'Drink warm herbal tea (chamomile, passionflower)',
            'Keep bedroom cool, dark, and quiet',
            'Use aromatherapy with lavender or sandalwood',
            'Practice gratitude or gentle journaling'
          ],
          exercise_guidelines: [
            'Moderate, consistent exercise is better than intense workouts',
            'Prefer activities like walking, swimming, cycling',
            'Practice yoga daily for flexibility and strength',
            'Exercise in the morning or early evening',
            'Avoid overexertion - listen to your body',
            'Include grounding activities like gardening',
            'Take rest days when needed'
          ]
        },
        herbal_remedies: [
          {
            herb: 'Ashwagandha',
            benefits: 'Reduces stress, improves energy, supports immune system',
            usage: '300-500mg with warm milk before bedtime',
            caution: 'Avoid during pregnancy, consult practitioner if on medications'
          },
          {
            herb: 'Brahmi',
            benefits: 'Enhances mental clarity, reduces anxiety, improves memory',
            usage: '250-500mg twice daily with meals'
          },
          {
            herb: 'Triphala',
            benefits: 'Supports digestion, detoxification, and regular elimination',
            usage: '1-2 tablets before bedtime with warm water'
          },
          {
            herb: 'Shatavari',
            benefits: 'Supports reproductive health, reduces stress, nourishes tissues',
            usage: '500mg twice daily with warm milk'
          },
          {
            herb: 'Tulsi (Holy Basil)',
            benefits: 'Boosts immunity, reduces stress, supports respiratory health',
            usage: 'Drink as tea 2-3 times daily'
          }
        ]
      };
      
      setRecommendations(mockRecommendations);
      setLoading(false);
    }, 2000);
  }, []);

  if (loading) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-4xl mx-auto text-center py-20"
      >
        <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-ayurveda-600 mx-auto mb-4"></div>
        <h2 className="text-2xl font-semibold text-gray-900 mb-2">Generating Your Personalized Recommendations</h2>
        <p className="text-gray-600">Analyzing your dosha constitution and health profile...</p>
      </motion.div>
    );
  }

  if (!recommendations) return null;

  const tabs = [
    { id: 'diet' as const, label: 'Diet & Nutrition', icon: Utensils },
    { id: 'yoga' as const, label: 'Yoga & Meditation', icon: Activity },
    { id: 'lifestyle' as const, label: 'Lifestyle', icon: Moon },
    { id: 'herbs' as const, label: 'Herbal Remedies', icon: Leaf }
  ];

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="max-w-6xl mx-auto"
    >
      {/* Header */}
      <div className="text-center mb-8">
        <Sparkles className="h-16 w-16 text-ayurveda-600 mx-auto mb-4" />
        <h1 className="text-4xl font-bold text-gray-900 font-serif mb-2">
          Your Personalized Recommendations
        </h1>
        <p className="text-lg text-gray-600">
          Customized guidance based on your dosha constitution and health profile
        </p>
      </div>

      {/* Tab Navigation */}
      <div className="bg-white rounded-2xl shadow-lg mb-8">
        <div className="border-b border-gray-200">
          <nav className="flex space-x-8 px-6">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`py-4 border-b-2 font-medium text-sm flex items-center space-x-2 ${
                    activeTab === tab.id
                      ? 'border-ayurveda-500 text-ayurveda-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  <Icon className="h-5 w-5" />
                  <span>{tab.label}</span>
                </button>
              );
            })}
          </nav>
        </div>

        <div className="p-8">
          {activeTab === 'diet' && (
            <motion.div
              key="diet"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.3 }}
            >
              <div className="grid md:grid-cols-2 gap-8 mb-8">
                <div className="bg-green-50 rounded-lg p-6">
                  <h3 className="text-lg font-bold text-green-900 mb-4">Foods to Include</h3>
                  <ul className="space-y-2">
                    {recommendations.diet.foods_to_include.map((food, index) => (
                      <li key={index} className="flex items-start">
                        <span className="text-green-600 mr-2">✓</span>
                        <span className="text-green-800">{food}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                <div className="bg-red-50 rounded-lg p-6">
                  <h3 className="text-lg font-bold text-red-900 mb-4">Foods to Avoid</h3>
                  <ul className="space-y-2">
                    {recommendations.diet.foods_to_avoid.map((food, index) => (
                      <li key={index} className="flex items-start">
                        <span className="text-red-600 mr-2">✗</span>
                        <span className="text-red-800">{food}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>

              <div className="grid md:grid-cols-2 gap-8">
                <div className="bg-blue-50 rounded-lg p-6">
                  <h3 className="text-lg font-bold text-blue-900 mb-3">Optimal Meal Timing</h3>
                  <p className="text-blue-800">{recommendations.diet.meal_timing}</p>
                </div>

                <div className="bg-purple-50 rounded-lg p-6">
                  <h3 className="text-lg font-bold text-purple-900 mb-3">Cooking Tips</h3>
                  <ul className="space-y-1">
                    {recommendations.diet.cooking_tips.map((tip, index) => (
                      <li key={index} className="text-purple-800 text-sm">• {tip}</li>
                    ))}
                  </ul>
                </div>
              </div>
            </motion.div>
          )}

          {activeTab === 'yoga' && (
            <motion.div
              key="yoga"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.3 }}
            >
              <div className="mb-8">
                <h3 className="text-xl font-bold text-gray-900 mb-6">Recommended Yoga Poses</h3>
                <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {recommendations.yoga.recommended_poses.map((pose, index) => (
                    <div key={index} className="bg-ayurveda-50 rounded-lg p-6">
                      <h4 className="font-semibold text-ayurveda-900 mb-2">{pose.name}</h4>
                      <p className="text-sm text-ayurveda-700 mb-2">{pose.benefits}</p>
                      <p className="text-xs text-ayurveda-600 font-medium">Duration: {pose.duration}</p>
                    </div>
                  ))}
                </div>
              </div>

              <div className="grid md:grid-cols-2 gap-8">
                <div className="bg-blue-50 rounded-lg p-6">
                  <h3 className="text-lg font-bold text-blue-900 mb-4">Breathing Exercises</h3>
                  <ul className="space-y-2">
                    {recommendations.yoga.breathing_exercises.map((exercise, index) => (
                      <li key={index} className="text-blue-800">• {exercise}</li>
                    ))}
                  </ul>
                </div>

                <div className="bg-purple-50 rounded-lg p-6">
                  <h3 className="text-lg font-bold text-purple-900 mb-3">Meditation Practice</h3>
                  <p className="text-purple-800">{recommendations.yoga.meditation_type}</p>
                </div>
              </div>
            </motion.div>
          )}

          {activeTab === 'lifestyle' && (
            <motion.div
              key="lifestyle"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.3 }}
            >
              <div className="space-y-8">
                <div className="bg-ayurveda-50 rounded-lg p-6">
                  <h3 className="text-lg font-bold text-ayurveda-900 mb-4">Daily Routine (Dinacharya)</h3>
                  <div className="grid md:grid-cols-2 gap-4">
                    {recommendations.lifestyle.daily_routine.map((item, index) => (
                      <div key={index} className="flex items-start">
                        <span className="text-ayurveda-600 mr-2">•</span>
                        <span className="text-ayurveda-800">{item}</span>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="grid md:grid-cols-2 gap-8">
                  <div className="bg-blue-50 rounded-lg p-6">
                    <h3 className="text-lg font-bold text-blue-900 mb-4">Sleep Recommendations</h3>
                    <ul className="space-y-2">
                      {recommendations.lifestyle.sleep_recommendations.map((rec, index) => (
                        <li key={index} className="flex items-start">
                          <span className="text-blue-600 mr-2">•</span>
                          <span className="text-blue-800 text-sm">{rec}</span>
                        </li>
                      ))}
                    </ul>
                  </div>

                  <div className="bg-green-50 rounded-lg p-6">
                    <h3 className="text-lg font-bold text-green-900 mb-4">Exercise Guidelines</h3>
                    <ul className="space-y-2">
                      {recommendations.lifestyle.exercise_guidelines.map((guideline, index) => (
                        <li key={index} className="flex items-start">
                          <span className="text-green-600 mr-2">•</span>
                          <span className="text-green-800 text-sm">{guideline}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>
            </motion.div>
          )}

          {activeTab === 'herbs' && (
            <motion.div
              key="herbs"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.3 }}
            >
              <div className="grid md:grid-cols-2 gap-6">
                {recommendations.herbal_remedies.map((remedy, index) => (
                  <div key={index} className="border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow">
                    <h4 className="text-lg font-bold text-ayurveda-900 mb-3">{remedy.herb}</h4>
                    <p className="text-gray-700 mb-3">{remedy.benefits}</p>
                    <div className="bg-ayurveda-50 rounded-lg p-3 mb-3">
                      <p className="text-sm text-ayurveda-800">
                        <strong>Usage:</strong> {remedy.usage}
                      </p>
                    </div>
                    {remedy.caution && (
                      <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-3">
                        <p className="text-xs text-yellow-800">
                          <strong>Caution:</strong> {remedy.caution}
                        </p>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </motion.div>
          )}
        </div>
      </div>

      {/* Disclaimer */}
      <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6">
        <h3 className="text-lg font-bold text-yellow-900 mb-2">Important Notice</h3>
        <p className="text-yellow-800">
          These recommendations are based on general Ayurvedic principles and your provided information. 
          For personalized treatment and before making significant changes to your diet or starting new 
          herbal supplements, please consult with a qualified Ayurvedic practitioner or healthcare professional. 
          Individual responses may vary, and what works for one person may not be suitable for another.
        </p>
      </div>
    </motion.div>
  );
};

export default PersonalizedRecommendations;