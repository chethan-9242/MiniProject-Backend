import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Leaf, Mail, Lock, User, ArrowRight, CheckCircle } from 'lucide-react';
import ThemeToggle from '../components/ThemeToggle';
import { useAuth } from '../contexts/AuthContext';

const Register: React.FC = () => {
  const navigate = useNavigate();
  const { register, isLoading } = useAuth();
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [confirm, setConfirm] = useState('');
  const [showConfirm, setShowConfirm] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [message, setMessage] = useState<string | null>(null);

  const passwordRules = {
    length: password.length >= 8,
    lower: /[a-z]/.test(password),
    upper: /[A-Z]/.test(password),
    digit: /\d/.test(password),
    symbol: /[^A-Za-z0-9]/.test(password),
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setMessage(null);

    if (password !== confirm) {
      setError('Passwords do not match');
      return;
    }

    const res = await register(name, email, password);
if (res.success) {
      setMessage('Registration successful! Please sign in.');
      setTimeout(() => navigate('/', { replace: true }), 800);
    } else {
      setError(res.message || 'Registration failed');
    }
  };

  return (
    <div className="relative min-h-screen overflow-hidden bg-gradient-to-br from-ayurveda-50 via-white to-ayurveda-100 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
      {/* Decorative blobs */}
      <div className="pointer-events-none absolute -left-24 -top-24 h-80 w-80 rounded-full bg-ayurveda-300/30 blur-3xl" />
      <div className="pointer-events-none absolute -right-24 -bottom-24 h-96 w-96 rounded-full bg-ayurveda-500/20 blur-3xl" />

      {/* Top bar */}
      <header className="sticky top-0 z-10 bg-transparent">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="bg-ayurveda-500 dark:bg-ayurveda-600 p-2 rounded-lg shadow-lg shadow-ayurveda-500/20">
              <Leaf className="h-7 w-7 text-white" />
            </div>
            <span className="text-xl font-bold text-ayurveda-900 dark:text-white font-serif">SwasthVedha</span>
          </div>
          <ThemeToggle />
        </div>
      </header>

      {/* Content */}
      <main className="relative z-0">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
          <div className="grid lg:grid-cols-2 gap-10 items-center">
            {/* Form card */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm rounded-3xl shadow-2xl border border-white/40 dark:border-white/10"
            >
              <div className="p-8 sm:p-10">
                <h1 className="text-3xl font-bold text-ayurveda-700 dark:text-ayurveda-300 text-center font-serif">Create your account</h1>
                <p className="mt-2 text-center text-gray-600 dark:text-gray-300">Join and unlock personalized Ayurvedic guidance</p>

                <form onSubmit={handleSubmit} className="mt-8 space-y-5">
                  {/* Name */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Full name</label>
                    <div className="relative">
                      <User className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" />
                      <input
                        type="text"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        className="w-full pl-10 pr-3 py-3 rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-ayurveda-500"
                        placeholder="Your full name"
                        required
                      />
                    </div>
                  </div>

                  {/* Email */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Email</label>
                    <div className="relative">
                      <Mail className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" />
                      <input
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        className="w-full pl-10 pr-3 py-3 rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-ayurveda-500"
                        placeholder="you@example.com"
                        required
                      />
                    </div>
                  </div>

                  {/* Password */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Password</label>
                    <div className="relative">
                      <Lock className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" />
                      <input
                        type={showPassword ? 'text' : 'password'}
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        className="w-full pl-10 pr-12 py-3 rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-ayurveda-500"
                        placeholder="••••••••"
                        required
                        minLength={6}
                      />
                      <button
                        type="button"
                        onClick={() => setShowPassword((v) => !v)}
                        className="absolute right-3 top-1/2 -translate-y-1/2 text-sm text-ayurveda-600 dark:text-ayurveda-400 hover:underline"
                      >
                        {showPassword ? 'Hide' : 'Show'}
                      </button>
                    </div>

                    {/* Password strength */}
                    <div className="mt-3 grid grid-cols-2 gap-x-4 gap-y-1 text-xs text-gray-600 dark:text-gray-300">
                      <div className={`flex items-center gap-2 ${passwordRules.length ? 'text-green-600 dark:text-green-400' : ''}`}>• 8+ characters</div>
                      <div className={`flex items-center gap-2 ${passwordRules.upper ? 'text-green-600 dark:text-green-400' : ''}`}>• Uppercase letter</div>
                      <div className={`flex items-center gap-2 ${passwordRules.lower ? 'text-green-600 dark:text-green-400' : ''}`}>• Lowercase letter</div>
                      <div className={`flex items-center gap-2 ${passwordRules.digit ? 'text-green-600 dark:text-green-400' : ''}`}>• Number</div>
                      <div className={`flex items-center gap-2 ${passwordRules.symbol ? 'text-green-600 dark:text-green-400' : ''}`}>• Symbol</div>
                    </div>
                  </div>

                  {/* Confirm */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Confirm password</label>
                    <div className="relative">
                      <Lock className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" />
                      <input
                        type={showConfirm ? 'text' : 'password'}
                        value={confirm}
                        onChange={(e) => setConfirm(e.target.value)}
                        className="w-full pl-10 pr-12 py-3 rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-ayurveda-500"
                        placeholder="••••••••"
                        required
                        minLength={6}
                      />
                      <button
                        type="button"
                        onClick={() => setShowConfirm((v) => !v)}
                        className="absolute right-3 top-1/2 -translate-y-1/2 text-sm text-ayurveda-600 dark:text-ayurveda-400 hover:underline"
                      >
                        {showConfirm ? 'Hide' : 'Show'}
                      </button>
                    </div>
                  </div>

                  {error && <div className="text-sm text-red-600 dark:text-red-400">{error}</div>}
                  {message && <div className="text-sm text-green-600 dark:text-green-400">{message}</div>}

                  <button
                    type="submit"
                    disabled={isLoading}
                    className="w-full inline-flex items-center justify-center gap-2 py-3 bg-ayurveda-600 hover:bg-ayurveda-700 text-white font-semibold rounded-xl transition-colors disabled:opacity-60 shadow-lg shadow-ayurveda-600/30"
                  >
                    {isLoading ? (
                      <>
                        <svg className="h-5 w-5 animate-spin" viewBox="0 0 24 24" aria-hidden="true"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"></path></svg>
                        <span>Creating account...</span>
                      </>
                    ) : (
                      <>
                        <span>Create Account</span>
                        <ArrowRight className="h-5 w-5" />
                      </>
                    )}
                  </button>
                </form>

                <p className="mt-6 text-center text-sm text-gray-600 dark:text-gray-300">
                  Already have an account?{' '}
                  <Link className="text-ayurveda-600 dark:text-ayurveda-400 font-medium hover:underline" to="/login">Sign in</Link>
                </p>
              </div>
            </motion.div>

            {/* Feature panel */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.7, delay: 0.1 }}
              className="hidden lg:block"
            >
              <div className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-ayurveda-500 to-ayurveda-700 p-10 text-white shadow-2xl">
                <div className="absolute -right-10 -top-10 h-40 w-40 rounded-full bg-white/10 blur-2xl" />
                <h2 className="text-3xl font-bold font-serif">Your Holistic Journey Starts Here</h2>
                <p className="mt-3 text-ayurveda-100">Create your account to personalize your health insights.</p>
                <ul className="mt-8 space-y-3 text-ayurveda-50">
                  <li className="flex items-start gap-3"><CheckCircle className="h-5 w-5 mt-0.5" /> Tailored dosha assessments</li>
                  <li className="flex items-start gap-3"><CheckCircle className="h-5 w-5 mt-0.5" /> AI symptom analysis</li>
                  <li className="flex items-start gap-3"><CheckCircle className="h-5 w-5 mt-0.5" /> Personalized diet & lifestyle plans</li>
                </ul>
              </div>
            </motion.div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="py-8 text-center text-sm text-gray-600 dark:text-gray-300">
        <div className="max-w-7xl mx-auto px-4">
          © {new Date().getFullYear()} SwasthVedha. All rights reserved.
        </div>
      </footer>
    </div>
  );
};

export default Register;
