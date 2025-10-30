import React from 'react';
import { motion } from 'framer-motion';
import { Sun, Moon } from 'lucide-react';
import { useTheme } from '../contexts/ThemeContext';

const ThemeToggle: React.FC = () => {
  const { isDarkMode, toggleTheme } = useTheme();

  const spring = {
    type: "spring" as const,
    stiffness: 700,
    damping: 30
  };

  return (
    <div className="relative">
      {/* Toggle Button */}
      <motion.button
        onClick={toggleTheme}
        className={`
          relative w-16 h-8 rounded-full p-1 cursor-pointer
          transition-all duration-500 ease-in-out
          focus:outline-none focus:ring-4 focus:ring-opacity-50
          theme-toggle-glow theme-toggle-focus btn-theme-toggle
          ${isDarkMode 
            ? 'bg-gradient-to-r from-cyan-400 to-cyan-600 shadow-cyan-400/50 shadow-lg focus:ring-cyan-400' 
            : 'bg-gradient-to-r from-blue-600 to-blue-800 shadow-blue-600/50 shadow-lg focus:ring-blue-400'
          }
        `}
        whileTap={{ scale: 0.95 }}
        whileHover={{ scale: 1.05 }}
        initial={false}
        animate={{
          backgroundColor: isDarkMode ? '#22d3ee' : '#1e40af',
        }}
        transition={{ duration: 0.5, ease: 'easeInOut' }}
      >
        {/* Glow Effect */}
        <div className={`
          absolute inset-0 rounded-full blur-sm opacity-60
          transition-all duration-500 ease-in-out
          ${isDarkMode 
            ? 'bg-gradient-to-r from-cyan-300 to-cyan-500' 
            : 'bg-gradient-to-r from-blue-500 to-blue-700'
          }
        `} />
        
        {/* Track */}
        <div className="relative w-full h-full">
          {/* Sliding Knob */}
          <motion.div
            className="
              absolute top-0 left-0 w-6 h-6 rounded-full
              bg-white shadow-lg
              flex items-center justify-center
              backdrop-blur-sm border border-white/20
            "
            layout
            transition={spring}
            initial={false}
            animate={{
              x: isDarkMode ? 32 : 0,
              rotate: isDarkMode ? 360 : 0,
            }}
            style={{
              boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15), 0 2px 4px rgba(0, 0, 0, 0.1)',
            }}
          >
            {/* Icon inside knob */}
            <motion.div
              initial={false}
              animate={{
                scale: isDarkMode ? 1 : 1,
                rotate: isDarkMode ? 0 : 0,
              }}
              transition={{ duration: 0.3, ease: 'easeInOut' }}
            >
              {isDarkMode ? (
                <Sun 
                  className="w-3 h-3 text-yellow-500" 
                  strokeWidth={3}
                />
              ) : (
                <Moon 
                  className="w-3 h-3 text-blue-600" 
                  strokeWidth={3}
                />
              )}
            </motion.div>
          </motion.div>

          {/* Background Icons */}
          <div className="absolute inset-0 flex items-center justify-between px-1">
            {/* Moon icon on left */}
            <motion.div
              initial={false}
              animate={{
                opacity: isDarkMode ? 0.3 : 0.8,
                scale: isDarkMode ? 0.8 : 1,
              }}
              transition={{ duration: 0.3 }}
              className="z-0"
            >
              <Moon className="w-3 h-3 text-white/80" strokeWidth={2} />
            </motion.div>
            
            {/* Sun icon on right */}
            <motion.div
              initial={false}
              animate={{
                opacity: isDarkMode ? 0.8 : 0.3,
                scale: isDarkMode ? 1 : 0.8,
              }}
              transition={{ duration: 0.3 }}
              className="z-0"
            >
              <Sun className="w-3 h-3 text-white/80" strokeWidth={2} />
            </motion.div>
          </div>
        </div>

        {/* Ripple Effect */}
        <motion.div
          className="absolute inset-0 rounded-full"
          initial={false}
          animate={{
            scale: [1, 1.2, 1],
            opacity: [0, 0.3, 0],
          }}
          transition={{
            duration: 0.6,
            ease: "easeOut",
            times: [0, 0.5, 1],
          }}
          key={isDarkMode ? 'dark' : 'light'}
          style={{
            background: isDarkMode 
              ? 'radial-gradient(circle, rgba(34, 211, 238, 0.4) 0%, transparent 70%)'
              : 'radial-gradient(circle, rgba(30, 64, 175, 0.4) 0%, transparent 70%)',
          }}
        />
      </motion.button>

      {/* Tooltip */}
      <motion.div
        className={`
          absolute top-full mt-2 left-1/2 transform -translate-x-1/2
          px-2 py-1 rounded text-xs font-medium
          pointer-events-none opacity-0 group-hover:opacity-100
          transition-opacity duration-200
          ${isDarkMode 
            ? 'bg-gray-800 text-white' 
            : 'bg-gray-700 text-white'
          }
        `}
        initial={{ opacity: 0, y: -5 }}
        whileHover={{ opacity: 1, y: 0 }}
      >
        {isDarkMode ? 'Light Mode' : 'Dark Mode'}
        <div className={`
          absolute -top-1 left-1/2 transform -translate-x-1/2
          w-2 h-2 rotate-45
          ${isDarkMode ? 'bg-gray-800' : 'bg-gray-700'}
        `} />
      </motion.div>
    </div>
  );
};

export default ThemeToggle;