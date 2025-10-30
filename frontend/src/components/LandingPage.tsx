import React, { useEffect } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { 
  Heart, 
  Brain, 
  Leaf, 
  Shield, 
  Sparkles,
  ArrowRight,
  CheckCircle,
  Scissors,
  MessageCircle
} from 'lucide-react';
import ThemeToggle from './ThemeToggle';

const LandingPage: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();

useEffect(() => {
    const params = new URLSearchParams(location.search);
    // Case 1: Popup flow set ?from=login; show landing briefly, then go to dashboard
    if (params.get('from') === 'login') {
      const t = setTimeout(() => navigate('/dashboard', { replace: true }), 1000);
      return () => clearTimeout(t);
    }
    // Case 2: Redirect flow set a localStorage flag; treat it the same
    try {
      const flag = localStorage.getItem('swasthvedha_after_login');
      if (flag === '1') {
        localStorage.removeItem('swasthvedha_after_login');
        const t = setTimeout(() => navigate('/dashboard', { replace: true }), 1000);
        return () => clearTimeout(t);
      }
    } catch {}
  }, [location.search, navigate]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-ayurveda-50 via-white to-ayurveda-100 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 transition-colors duration-500">
      {/* Navigation */}
      <nav className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-md shadow-sm fixed w-full top-0 z-50 transition-colors duration-500">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center space-x-3">
              <div className="bg-ayurveda-500 dark:bg-ayurveda-600 p-2 rounded-lg transition-colors">
                <Leaf className="h-8 w-8 text-white" />
              </div>
              <h1 className="text-2xl font-bold text-ayurveda-900 dark:text-white font-serif transition-colors">SwasthVedha</h1>
            </div>
            <div className="flex items-center space-x-8">
              <div className="hidden md:flex space-x-8">
                <a href="#features" className="text-gray-700 dark:text-gray-300 hover:text-ayurveda-600 dark:hover:text-ayurveda-400 transition-colors">Features</a>
                <a href="#about" className="text-gray-700 dark:text-gray-300 hover:text-ayurveda-600 dark:hover:text-ayurveda-400 transition-colors">About</a>
                <a href="#contact" className="text-gray-700 dark:text-gray-300 hover:text-ayurveda-600 dark:hover:text-ayurveda-400 transition-colors">Contact</a>
              </div>
              <ThemeToggle />
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <motion.div
              initial={{ opacity: 0, y: 50 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
              className="text-center lg:text-left"
            >
              <h1 className="text-5xl lg:text-6xl font-bold text-gray-900 dark:text-white font-serif mb-6 transition-colors">
                Your AI-Powered
                <span className="block text-ayurveda-600 dark:text-ayurveda-400">Ayurvedic</span>
                Healthcare Assistant
              </h1>
              <p className="text-xl text-gray-600 dark:text-gray-300 mb-8 leading-relaxed transition-colors">
                SwasthVedha integrates ancient Ayurvedic wisdom with cutting-edge AI technology 
                to provide personalized health insights, dosha analysis, symptom checking, and 
                holistic wellness guidance.
              </p>
              
              <div className="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
                <Link
                  to="/dashboard"
                  className="inline-flex items-center px-8 py-4 bg-ayurveda-600 text-white font-semibold rounded-full hover:bg-ayurveda-700 transition-colors shadow-lg hover:shadow-xl transform hover:scale-105 duration-200"
                >
                  Get Started
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Link>
                <button className="inline-flex items-center px-8 py-4 border-2 border-ayurveda-600 text-ayurveda-600 font-semibold rounded-full hover:bg-ayurveda-50 transition-colors">
                  Learn More
                </button>
              </div>

              <div className="mt-12 grid grid-cols-3 gap-8">
                <div className="text-center">
                  <div className="text-2xl font-bold text-ayurveda-600 dark:text-ayurveda-400 transition-colors">5000+</div>
                  <div className="text-sm text-gray-600 dark:text-gray-300 transition-colors">Users Served</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-ayurveda-600 dark:text-ayurveda-400 transition-colors">98%</div>
                  <div className="text-sm text-gray-600 dark:text-gray-300 transition-colors">Accuracy</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-ayurveda-600 dark:text-ayurveda-400 transition-colors">24/7</div>
                  <div className="text-sm text-gray-600 dark:text-gray-300 transition-colors">Available</div>
                </div>
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.8, delay: 0.2 }}
              className="relative"
            >
              <div className="bg-gradient-to-br from-ayurveda-400 to-ayurveda-600 rounded-3xl p-8 shadow-2xl">
                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-white/90 rounded-2xl p-4 text-center">
                    <Heart className="h-8 w-8 text-ayurveda-500 mx-auto mb-2" />
                    <div className="font-semibold text-gray-800">Dosha Analysis</div>
                  </div>
                  <div className="bg-white/90 rounded-2xl p-4 text-center">
                    <Brain className="h-8 w-8 text-ayurveda-500 mx-auto mb-2" />
                    <div className="font-semibold text-gray-800">AI Diagnosis</div>
                  </div>
                  <div className="bg-white/90 rounded-2xl p-4 text-center">
                    <Shield className="h-8 w-8 text-ayurveda-500 mx-auto mb-2" />
                    <div className="font-semibold text-gray-800">Skin Detection</div>
                  </div>
                  <div className="bg-white/90 rounded-2xl p-4 text-center">
                    <Scissors className="h-8 w-8 text-ayurveda-500 mx-auto mb-2" />
                    <div className="font-semibold text-gray-800">Hair & Scalp Care</div>
                  </div>
                  <div className="bg-white/90 rounded-2xl p-4 text-center">
                    <MessageCircle className="h-8 w-8 text-ayurveda-500 mx-auto mb-2" />
                    <div className="font-semibold text-gray-800">AI Chatbot</div>
                  </div>
                  <div className="bg-white/90 rounded-2xl p-4 text-center">
                    <Sparkles className="h-8 w-8 text-ayurveda-500 mx-auto mb-2" />
                    <div className="font-semibold text-gray-800">Personalized Care</div>
                  </div>
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 font-serif mb-4">
              Comprehensive Ayurvedic Healthcare Modules
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Experience the power of ancient wisdom combined with modern AI technology 
              through our integrated healthcare modules.
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              className="bg-gradient-to-br from-vata to-white p-6 rounded-2xl shadow-lg hover:shadow-xl transition-shadow"
            >
              <Heart className="h-12 w-12 text-ayurveda-600 mb-4" />
              <h3 className="text-xl font-semibold mb-3">Dosha Classification</h3>
              <p className="text-gray-600 mb-4">
                Analyze your Vata, Pitta, and Kapha doshas using Decision Trees and 43 comprehensive parameters.
              </p>
              <ul className="space-y-2">
                <li className="flex items-center text-sm text-gray-600">
                  <CheckCircle className="h-4 w-4 text-ayurveda-500 mr-2" />
                  Digestion analysis
                </li>
                <li className="flex items-center text-sm text-gray-600">
                  <CheckCircle className="h-4 w-4 text-ayurveda-500 mr-2" />
                  Sleep pattern evaluation
                </li>
              </ul>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.1 }}
              className="bg-gradient-to-br from-pitta to-white p-6 rounded-2xl shadow-lg hover:shadow-xl transition-shadow"
            >
              <Brain className="h-12 w-12 text-ayurveda-600 mb-4" />
              <h3 className="text-xl font-semibold mb-3">AI Symptom Checker</h3>
              <p className="text-gray-600 mb-4">
                Fine-tuned LLM models analyze symptoms based on Charaka Samhita knowledge.
              </p>
              <ul className="space-y-2">
                <li className="flex items-center text-sm text-gray-600">
                  <CheckCircle className="h-4 w-4 text-ayurveda-500 mr-2" />
                  Natural language processing
                </li>
                <li className="flex items-center text-sm text-gray-600">
                  <CheckCircle className="h-4 w-4 text-ayurveda-500 mr-2" />
                  Traditional remedy suggestions
                </li>
              </ul>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="bg-gradient-to-br from-kapha to-white p-6 rounded-2xl shadow-lg hover:shadow-xl transition-shadow"
            >
              <Shield className="h-12 w-12 text-ayurveda-600 mb-4" />
              <h3 className="text-xl font-semibold mb-3">Skin Disease Detection</h3>
              <p className="text-gray-600 mb-4">
                CNN-based medical image analysis for detecting 22 categories of skin conditions.
              </p>
              <ul className="space-y-2">
                <li className="flex items-center text-sm text-gray-600">
                  <CheckCircle className="h-4 w-4 text-ayurveda-500 mr-2" />
                  Image-based diagnosis
                </li>
                <li className="flex items-center text-sm text-gray-600">
                  <CheckCircle className="h-4 w-4 text-ayurveda-500 mr-2" />
                  Ayurvedic treatment options
                </li>
              </ul>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.3 }}
              className="bg-gradient-to-br from-ayurveda-100 to-white p-6 rounded-2xl shadow-lg hover:shadow-xl transition-shadow"
            >
              <MessageCircle className="h-12 w-12 text-ayurveda-600 mb-4" />
              <h3 className="text-xl font-semibold mb-3">Healthcare Chatbot</h3>
              <p className="text-gray-600 mb-4">
                Intelligent chatbot providing gentle, safe first aid measures and personalized guidance.
              </p>
              <ul className="space-y-2">
                <li className="flex items-center text-sm text-gray-600">
                  <CheckCircle className="h-4 w-4 text-ayurveda-500 mr-2" />
                  Context-aware responses
                </li>
                <li className="flex items-center text-sm text-gray-600">
                  <CheckCircle className="h-4 w-4 text-ayurveda-500 mr-2" />
                  24/7 availability
                </li>
              </ul>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.4 }}
              className="bg-gradient-to-br from-ayurveda-200 to-white p-6 rounded-2xl shadow-lg hover:shadow-xl transition-shadow"
            >
              <Sparkles className="h-12 w-12 text-ayurveda-600 mb-4" />
              <h3 className="text-xl font-semibold mb-3">Personalized Recommendations</h3>
              <p className="text-gray-600 mb-4">
                Customized diet, yoga, and lifestyle recommendations based on your dosha and health profile.
              </p>
              <ul className="space-y-2">
                <li className="flex items-center text-sm text-gray-600">
                  <CheckCircle className="h-4 w-4 text-ayurveda-500 mr-2" />
                  Personalized diet plans
                </li>
                <li className="flex items-center text-sm text-gray-600">
                  <CheckCircle className="h-4 w-4 text-ayurveda-500 mr-2" />
                  Yoga routines
                </li>
              </ul>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.5 }}
              className="bg-gradient-to-br from-teal-100 to-white p-6 rounded-2xl shadow-lg hover:shadow-xl transition-shadow"
            >
              <Scissors className="h-12 w-12 text-ayurveda-600 mb-4" />
              <h3 className="text-xl font-semibold mb-3">Hair & Scalp Disorders</h3>
              <p className="text-gray-600 mb-4">
                AI-powered hair and scalp condition detection with comprehensive Ayurvedic treatment plans.
              </p>
              <ul className="space-y-2">
                <li className="flex items-center text-sm text-gray-600">
                  <CheckCircle className="h-4 w-4 text-ayurveda-500 mr-2" />
                  Image-based analysis
                </li>
                <li className="flex items-center text-sm text-gray-600">
                  <CheckCircle className="h-4 w-4 text-ayurveda-500 mr-2" />
                  Dosha-based treatments
                </li>
              </ul>
            </motion.div>
          </div>
        </div>
      </section>

      {/* About Section */}
      <section id="about" className="py-20 bg-ayurveda-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <motion.div
              initial={{ opacity: 0, x: -50 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8 }}
            >
              <h2 className="text-4xl font-bold text-gray-900 font-serif mb-6">
                Bridging Ancient Wisdom with Modern Technology
              </h2>
              <p className="text-lg text-gray-700 mb-6 leading-relaxed">
                SwasthVedha represents a revolutionary approach to healthcare by combining the 
                time-tested principles of Ayurveda with cutting-edge AI and machine learning technologies. 
                Our platform makes ancient texts like Charaka Samhita and Sushruta Samhita accessible 
                to modern users through digital transformation.
              </p>
              <p className="text-lg text-gray-700 mb-8 leading-relaxed">
                Unlike isolated health apps, SwasthVedha integrates multiple AI components into a 
                single user-centric platform, providing comprehensive healthcare guidance while 
                preserving and promoting our cultural heritage.
              </p>
              <Link
                to="/dashboard"
                className="inline-flex items-center px-6 py-3 bg-ayurveda-600 text-white font-semibold rounded-full hover:bg-ayurveda-700 transition-colors"
              >
                Explore Platform
                <ArrowRight className="ml-2 h-5 w-5" />
              </Link>
            </motion.div>
            
            <motion.div
              initial={{ opacity: 0, x: 50 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8 }}
              className="bg-white rounded-3xl p-8 shadow-xl"
            >
              <h3 className="text-2xl font-bold text-gray-900 mb-6">Key Benefits</h3>
              <div className="space-y-4">
                <div className="flex items-start">
                  <CheckCircle className="h-6 w-6 text-ayurveda-500 mr-3 mt-0.5" />
                  <div>
                    <h4 className="font-semibold text-gray-900">Personalized Healthcare</h4>
                    <p className="text-gray-600">Tailored recommendations based on your unique dosha constitution</p>
                  </div>
                </div>
                <div className="flex items-start">
                  <CheckCircle className="h-6 w-6 text-ayurveda-500 mr-3 mt-0.5" />
                  <div>
                    <h4 className="font-semibold text-gray-900">Cultural Preservation</h4>
                    <p className="text-gray-600">Digital preservation of ancient Ayurvedic knowledge for future generations</p>
                  </div>
                </div>
                <div className="flex items-start">
                  <CheckCircle className="h-6 w-6 text-ayurveda-500 mr-3 mt-0.5" />
                  <div>
                    <h4 className="font-semibold text-gray-900">Preventive Care</h4>
                    <p className="text-gray-600">Focus on prevention and early intervention for better health outcomes</p>
                  </div>
                </div>
                <div className="flex items-start">
                  <CheckCircle className="h-6 w-6 text-ayurveda-500 mr-3 mt-0.5" />
                  <div>
                    <h4 className="font-semibold text-gray-900">Doctor Assistance</h4>
                    <p className="text-gray-600">Supporting healthcare professionals with preliminary assessments</p>
                  </div>
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-ayurveda-600 to-ayurveda-700">
        <div className="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <h2 className="text-4xl font-bold text-white font-serif mb-6">
              Start Your Ayurvedic Wellness Journey Today
            </h2>
            <p className="text-xl text-ayurveda-100 mb-8">
              Experience personalized healthcare guidance powered by AI and rooted in ancient wisdom
            </p>
            <Link
              to="/dashboard"
              className="inline-flex items-center px-8 py-4 bg-white text-ayurveda-600 font-bold rounded-full hover:bg-ayurveda-50 transition-colors shadow-lg hover:shadow-xl transform hover:scale-105 duration-200"
            >
              Get Started Now
              <ArrowRight className="ml-2 h-5 w-5" />
            </Link>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-3 gap-8">
            <div>
              <div className="flex items-center space-x-3 mb-4">
                <div className="bg-ayurveda-500 p-2 rounded-lg">
                  <Leaf className="h-6 w-6 text-white" />
                </div>
                <h3 className="text-xl font-bold font-serif">SwasthVedha</h3>
              </div>
              <p className="text-gray-400">
                AI-driven Ayurvedic healthcare assistant combining ancient wisdom with modern technology.
              </p>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Quick Links</h4>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#features" className="hover:text-white transition-colors">Features</a></li>
                <li><a href="#about" className="hover:text-white transition-colors">About</a></li>
                <li><Link to="/dashboard" className="hover:text-white transition-colors">Dashboard</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Contact</h4>
              <p className="text-gray-400">
                Email: info@swasthvedha.com<br />
                Phone: +91 12345 67890
              </p>
            </div>
          </div>
          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
            <p>&copy; 2024 SwasthVedha. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;