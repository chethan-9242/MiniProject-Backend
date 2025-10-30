import React from 'react';
import { motion } from 'framer-motion';
import { 
  Sun, 
  Moon, 
  Palette, 
  Eye, 
  Heart, 
  Star,
  Zap,
  Shield
} from 'lucide-react';
import ThemeToggle from './ThemeToggle';
import { useTheme } from '../contexts/ThemeContext';

const ThemeDemo: React.FC = () => {
  const { isDarkMode } = useTheme();

  const features = [
    {
      icon: Sun,
      title: 'Light Mode',
      description: 'Clean and bright interface for optimal visibility during daytime use.',
      color: 'from-yellow-400 to-orange-500'
    },
    {
      icon: Moon,
      title: 'Dark Mode',
      description: 'Easy on the eyes with reduced blue light for comfortable nighttime usage.',
      color: 'from-blue-600 to-purple-700'
    },
    {
      icon: Palette,
      title: 'Smooth Transitions',
      description: 'Seamless color transitions with beautiful animations throughout the interface.',
      color: 'from-purple-500 to-pink-600'
    },
    {
      icon: Eye,
      title: 'Accessibility',
      description: 'Designed with accessibility in mind, following WCAG guidelines.',
      color: 'from-green-500 to-teal-600'
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-ayurveda-50 via-white to-ayurveda-100 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 transition-colors duration-500">
      {/* Header */}
      <header className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-md shadow-sm border-b border-gray-200 dark:border-gray-700 transition-colors duration-500">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center space-x-3">
              <div className="bg-ayurveda-500 dark:bg-ayurveda-600 p-2 rounded-lg transition-colors">
                <Zap className="h-8 w-8 text-white" />
              </div>
              <h1 className="text-2xl font-bold text-ayurveda-900 dark:text-white font-serif transition-colors">
                Theme Demo
              </h1>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-600 dark:text-gray-300 transition-colors">
                {isDarkMode ? 'Dark Mode' : 'Light Mode'}
              </span>
              <ThemeToggle />
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Hero Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-16"
        >
          <h1 className="text-4xl lg:text-6xl font-bold text-gray-900 dark:text-white font-serif mb-6 transition-colors">
            Beautiful Dark Mode
            <span className="block text-ayurveda-600 dark:text-ayurveda-400">Toggle Demo</span>
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto mb-8 transition-colors">
            Experience our sleek dark mode toggle with smooth animations, glowing effects, 
            and seamless color transitions across the entire interface.
          </p>
          
          {/* Demo Stats */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <motion.div
              whileHover={{ scale: 1.05 }}
              className="bg-white dark:bg-gray-800 rounded-2xl p-6 shadow-lg transition-colors duration-500"
            >
              <Heart className="h-8 w-8 text-red-500 mx-auto mb-3" />
              <div className="text-2xl font-bold text-gray-900 dark:text-white transition-colors">500ms</div>
              <div className="text-sm text-gray-600 dark:text-gray-300 transition-colors">Transition Duration</div>
            </motion.div>
            
            <motion.div
              whileHover={{ scale: 1.05 }}
              className="bg-white dark:bg-gray-800 rounded-2xl p-6 shadow-lg transition-colors duration-500"
            >
              <Star className="h-8 w-8 text-yellow-500 mx-auto mb-3" />
              <div className="text-2xl font-bold text-gray-900 dark:text-white transition-colors">100%</div>
              <div className="text-sm text-gray-600 dark:text-gray-300 transition-colors">Responsive Design</div>
            </motion.div>
            
            <motion.div
              whileHover={{ scale: 1.05 }}
              className="bg-white dark:bg-gray-800 rounded-2xl p-6 shadow-lg transition-colors duration-500"
            >
              <Shield className="h-8 w-8 text-green-500 mx-auto mb-3" />
              <div className="text-2xl font-bold text-gray-900 dark:text-white transition-colors">WCAG</div>
              <div className="text-sm text-gray-600 dark:text-gray-300 transition-colors">Accessibility Ready</div>
            </motion.div>
          </div>
        </motion.div>

        {/* Features Grid */}
        <div className="grid md:grid-cols-2 gap-8 mb-16">
          {features.map((feature, index) => (
            <motion.div
              key={feature.title}
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
              whileHover={{ scale: 1.02 }}
              className="bg-white dark:bg-gray-800 rounded-2xl p-8 shadow-lg hover:shadow-xl transition-all duration-500"
            >
              <div className={`w-14 h-14 rounded-full bg-gradient-to-r ${feature.color} p-3 mb-6`}>
                <feature.icon className="h-8 w-8 text-white" />
              </div>
              <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-4 transition-colors">
                {feature.title}
              </h3>
              <p className="text-gray-600 dark:text-gray-300 transition-colors">
                {feature.description}
              </p>
            </motion.div>
          ))}
        </div>

        {/* Interactive Demo Section */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          className="bg-gradient-to-br from-ayurveda-500 to-ayurveda-700 dark:from-gray-700 dark:to-gray-900 rounded-3xl p-8 text-center transition-colors duration-500"
        >
          <h2 className="text-3xl font-bold text-white mb-4 font-serif">
            Try the Toggle Above!
          </h2>
          <p className="text-ayurveda-100 dark:text-gray-300 mb-8 text-lg transition-colors">
            Click the beautiful switch in the top-right corner to experience 
            the smooth transition between light and dark modes.
          </p>
          
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-white/10 backdrop-blur-sm rounded-xl p-4">
              <div className="text-2xl font-bold text-white">✨</div>
              <div className="text-white/90 text-sm">Smooth</div>
            </div>
            <div className="bg-white/10 backdrop-blur-sm rounded-xl p-4">
              <div className="text-2xl font-bold text-white">🎨</div>
              <div className="text-white/90 text-sm">Beautiful</div>
            </div>
            <div className="bg-white/10 backdrop-blur-sm rounded-xl p-4">
              <div className="text-2xl font-bold text-white">⚡</div>
              <div className="text-white/90 text-sm">Fast</div>
            </div>
            <div className="bg-white/10 backdrop-blur-sm rounded-xl p-4">
              <div className="text-2xl font-bold text-white">♿</div>
              <div className="text-white/90 text-sm">Accessible</div>
            </div>
          </div>
        </motion.div>

        {/* Code Preview */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.8 }}
          className="mt-16 bg-white dark:bg-gray-800 rounded-2xl p-8 shadow-lg transition-colors duration-500"
        >
          <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-6 transition-colors">
            How to Use
          </h3>
          <div className="bg-gray-100 dark:bg-gray-900 rounded-xl p-6 overflow-x-auto transition-colors duration-500">
            <pre className="text-sm text-gray-800 dark:text-gray-200 transition-colors">
              <code>{`import ThemeToggle from './components/ThemeToggle';
import { ThemeProvider } from './contexts/ThemeContext';

function App() {
  return (
    <ThemeProvider>
      <div className="bg-white dark:bg-gray-800">
        <ThemeToggle />
        {/* Your app content */}
      </div>
    </ThemeProvider>
  );
}`}</code>
            </pre>
          </div>
        </motion.div>
      </main>
    </div>
  );
};

export default ThemeDemo;