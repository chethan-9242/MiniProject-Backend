import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  Heart, 
  Brain, 
  Shield, 
  MessageCircle, 
  Sparkles, 
  Leaf,
  User,
  Settings,
  Bell,
  Menu,
  X,
  Scissors
} from 'lucide-react';
import ThemeToggle from './ThemeToggle';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';

// Import individual module components (we'll create these)
import DoshaClassificationNew from './modules/DoshaClassification_New';
import SymptomChecker from './modules/SymptomChecker';
import SkinDiseaseDetection from './modules/SkinDiseaseDetection';
import PersonalizedRecommendations from './modules/PersonalizedRecommendations';
import HairScalpDisorders from './modules/HairScalpDisorders';
import FloatingChat from './FloatingChat';

interface ModuleCardProps {
  icon: React.ElementType;
  title: string;
  description: string;
  color: string;
  isActive: boolean;
  onClick: () => void;
}

const ModuleCard: React.FC<ModuleCardProps> = ({ icon: Icon, title, description, color, isActive, onClick }) => (
  <motion.div
    whileHover={{ scale: 1.02 }}
    whileTap={{ scale: 0.98 }}
    className={`p-6 rounded-2xl cursor-pointer transition-all duration-200 shadow-lg hover:shadow-xl ${
      isActive 
        ? `bg-gradient-to-br ${color} text-white shadow-2xl` 
        : 'bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700'
    }`}
    onClick={onClick}
  >
    <Icon className={`h-12 w-12 mb-4 ${isActive ? 'text-white' : 'text-ayurveda-600 dark:text-ayurveda-400'}`} />
    <h3 className={`text-xl font-semibold mb-2 ${isActive ? 'text-white' : 'text-gray-900 dark:text-white'}`}>
      {title}
    </h3>
    <p className={`text-sm ${isActive ? 'text-white/90' : 'text-gray-600 dark:text-gray-300'}`}>
      {description}
    </p>
  </motion.div>
);

const Dashboard: React.FC = () => {
  const [activeModule, setActiveModule] = useState<string | null>(null);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const modules = [
    {
      id: 'dosha',
      title: 'Dosha Classification',
      description: '10 essential questions · AI-powered with Google Flan-T5 · Personalized recommendations',
      icon: Heart,
      color: 'from-red-500 to-pink-600',
      component: DoshaClassificationNew
    },
    {
      id: 'symptoms',
      title: 'Symptom Checker',
      description: 'AI-powered symptom analysis based on Ayurvedic principles and modern medicine',
      icon: Brain,
      color: 'from-blue-500 to-indigo-600',
      component: SymptomChecker
    },
    {
      id: 'skin',
      title: 'Skin Disease Detection',
      description: 'Upload images for CNN-based skin condition analysis and Ayurvedic treatment suggestions',
      icon: Shield,
      color: 'from-green-500 to-emerald-600',
      component: SkinDiseaseDetection
    },
    {
      id: 'hair',
      title: 'Hair & Scalp Disorders',
      description: 'AI-powered hair and scalp condition detection with comprehensive Ayurvedic treatment plans',
      icon: Scissors,
      color: 'from-teal-500 to-cyan-600',
      component: HairScalpDisorders
    },
    {
      id: 'recommendations',
      title: 'Personalized Recommendations',
      description: 'Receive customized diet, yoga, and lifestyle recommendations based on your profile',
      icon: Sparkles,
      color: 'from-yellow-500 to-orange-600',
      component: PersonalizedRecommendations
    }
  ];

  const renderActiveModule = () => {
    const module = modules.find(m => m.id === activeModule);
    if (!module) return null;
    
    const Component = module.component;
    return <Component />;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-ayurveda-50 via-white to-ayurveda-100 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 transition-colors duration-500">
      {/* Header */}
      <header className="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700 transition-colors duration-500">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center space-x-4">
              <button
                onClick={() => setSidebarOpen(!sidebarOpen)}
                className="lg:hidden p-2 rounded-md text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
              >
                {sidebarOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
              </button>
              
              <div className="flex items-center space-x-3">
                <div className="bg-ayurveda-500 dark:bg-ayurveda-600 p-2 rounded-lg transition-colors">
                  <Leaf className="h-8 w-8 text-white" />
                </div>
                <div>
                  <h1 className="text-2xl font-bold text-ayurveda-900 dark:text-white font-serif transition-colors">SwasthVedha</h1>
                  <p className="text-sm text-gray-600 dark:text-gray-300 transition-colors">AI-Powered Ayurvedic Healthcare</p>
                </div>
              </div>
            </div>

            <div className="flex items-center space-x-4">
              <ThemeToggle />
              <button className="p-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-full transition-colors">
                <Bell className="h-6 w-6" />
              </button>
              <button className="p-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-full transition-colors">
                <Settings className="h-6 w-6" />
              </button>
              <div className="flex items-center gap-2">
                <div className="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-full bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200">
                  <User className="h-5 w-5" />
                  <span className="text-sm font-medium truncate max-w-[140px]">{user?.name || 'User'}</span>
                </div>
                <button
                  onClick={() => { logout(); navigate('/login', { replace: true }); }}
                  className="px-3 py-1.5 rounded-full bg-ayurveda-600 text-white text-sm font-medium hover:bg-ayurveda-700 transition-colors"
                >
                  Logout
                </button>
              </div>
            </div>
          </div>
        </div>
      </header>

      <div className="flex">
        {/* Sidebar */}
        <motion.div
          initial={false}
          animate={{
            width: sidebarOpen ? '280px' : '0px',
            opacity: sidebarOpen ? 1 : 0
          }}
          className="lg:hidden fixed inset-y-0 left-0 z-50 bg-white dark:bg-gray-800 shadow-xl overflow-hidden transition-colors duration-500"
        >
          <div className="p-6">
            <nav className="space-y-2">
              {modules.map((module) => (
                <button
                  key={module.id}
                  onClick={() => {
                    setActiveModule(module.id);
                    setSidebarOpen(false);
                  }}
                  className={`w-full text-left p-3 rounded-lg transition-colors ${
                    activeModule === module.id
                      ? 'bg-ayurveda-100 dark:bg-ayurveda-900 text-ayurveda-800 dark:text-ayurveda-200'
                      : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
                  }`}
                >
                  <div className="flex items-center space-x-3">
                    <module.icon className="h-5 w-5" />
                    <span className="font-medium">{module.title}</span>
                  </div>
                </button>
              ))}
            </nav>
          </div>
        </motion.div>

        {/* Main Content */}
        <main className="flex-1 p-6">
          {activeModule ? (
            <motion.div
              key={activeModule}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
            >
              <div className="max-w-7xl mx-auto">
                {/* Module Header */}
                <div className="mb-8">
                  <button
                    onClick={() => setActiveModule(null)}
                    className="mb-4 text-ayurveda-600 dark:text-ayurveda-400 hover:text-ayurveda-800 dark:hover:text-ayurveda-200 font-medium flex items-center transition-colors"
                  >
                    ← Back to Modules
                  </button>
                  {renderActiveModule()}
                </div>
              </div>
            </motion.div>
          ) : (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="max-w-7xl mx-auto"
            >
              {/* Welcome Section */}
              <div className="text-center mb-12">
                <motion.h1
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="text-4xl lg:text-5xl font-bold text-gray-900 dark:text-white font-serif mb-4 transition-colors"
                >
                  Welcome to Your Ayurvedic Health Dashboard
                </motion.h1>
                <motion.p
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.1 }}
                  className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto transition-colors"
                >
                  Explore our comprehensive suite of AI-powered Ayurvedic healthcare modules 
                  designed to provide personalized insights and guidance for your wellness journey.
                </motion.p>
              </div>

              {/* Quick Stats */}
              <motion.div
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 }}
                className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12"
              >
                <div className="bg-white dark:bg-gray-800 rounded-2xl p-6 shadow-lg text-center transition-colors duration-500">
                  <div className="text-3xl font-bold text-ayurveda-600 dark:text-ayurveda-400 mb-2 transition-colors">5</div>
                  <div className="text-gray-600 dark:text-gray-300 transition-colors">AI Modules</div>
                </div>
                <div className="bg-white dark:bg-gray-800 rounded-2xl p-6 shadow-lg text-center transition-colors duration-500">
                  <div className="text-3xl font-bold text-ayurveda-600 dark:text-ayurveda-400 mb-2 transition-colors">43</div>
                  <div className="text-gray-600 dark:text-gray-300 transition-colors">Assessment Parameters</div>
                </div>
                <div className="bg-white dark:bg-gray-800 rounded-2xl p-6 shadow-lg text-center transition-colors duration-500">
                  <div className="text-3xl font-bold text-ayurveda-600 dark:text-ayurveda-400 mb-2 transition-colors">24/7</div>
                  <div className="text-gray-600 dark:text-gray-300 transition-colors">AI Assistance</div>
                </div>
              </motion.div>

              {/* Module Grid */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
                {modules.map((module, index) => (
                  <motion.div
                    key={module.id}
                    initial={{ opacity: 0, y: 30 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.3 + index * 0.1 }}
                  >
                    <ModuleCard
                      icon={module.icon}
                      title={module.title}
                      description={module.description}
                      color={module.color}
                      isActive={false}
                      onClick={() => setActiveModule(module.id)}
                    />
                  </motion.div>
                ))}
              </div>

            </motion.div>
          )}
        </main>
      </div>
      
      {/* Floating Chat Component */}
      <FloatingChat />
    </div>
  );
};

export default Dashboard;