import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Leaf, Mail, Lock, ArrowRight } from 'lucide-react';
import ThemeToggle from '../components/ThemeToggle';
import { useAuth } from '../contexts/AuthContext';

const Login: React.FC = () => {
  const navigate = useNavigate();
  const { login, loginWithGoogle, loginWithFacebook, isLoading } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState<string | null>(null);

const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    const res = await login(email, password);
    if (res.success) {
      navigate('/?from=login', { replace: true }); // show Landing then redirect to dashboard
    } else {
      setError(res.message || 'Login failed');
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
                <h1 className="text-3xl font-bold text-ayurveda-700 dark:text-ayurveda-300 text-center font-serif">Welcome back</h1>
                <p className="mt-2 text-center text-gray-600 dark:text-gray-300">Sign in to continue your wellness journey</p>

                <form onSubmit={handleSubmit} className="mt-8 space-y-5">
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
                      />
                      <button
                        type="button"
                        onClick={() => setShowPassword((v) => !v)}
                        className="absolute right-3 top-1/2 -translate-y-1/2 text-sm text-ayurveda-600 dark:text-ayurveda-400 hover:underline"
                      >
                        {showPassword ? 'Hide' : 'Show'}
                      </button>
                    </div>
                    <div className="mt-2 flex items-center justify-between text-sm">
                      <label className="inline-flex items-center gap-2 text-gray-600 dark:text-gray-300">
                        <input type="checkbox" className="rounded border-gray-300 dark:border-gray-700 text-ayurveda-600 focus:ring-ayurveda-500" />
                        Remember me
                      </label>
                      <span className="text-ayurveda-600 dark:text-ayurveda-400 hover:underline cursor-pointer">Forgot password?</span>
                    </div>
                  </div>

                  {error && (
                    <div className="text-sm text-red-600 dark:text-red-400">{error}</div>
                  )}

                  <button
                    type="submit"
                    disabled={isLoading}
                    className="w-full inline-flex items-center justify-center gap-2 py-3 bg-ayurveda-600 hover:bg-ayurveda-700 text-white font-semibold rounded-xl transition-colors disabled:opacity-60 shadow-lg shadow-ayurveda-600/30"
                  >
                    {isLoading ? (
                      <>
                        <svg className="h-5 w-5 animate-spin" viewBox="0 0 24 24" aria-hidden="true"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"></path></svg>
                        <span>Signing in...</span>
                      </>
                    ) : (
                      <>
                        <span>Sign In</span>
                        <ArrowRight className="h-5 w-5" />
                      </>
                    )}
                  </button>
                </form>

                {/* Social sign-in */}
                <div className="mt-6">
                  <div className="relative py-3 text-center text-sm text-gray-500 dark:text-gray-400">
                    <span className="bg-white dark:bg-gray-800 px-2 relative z-10">or continue with</span>
                    <div className="absolute inset-x-0 top-1/2 -translate-y-1/2 border-t border-gray-200 dark:border-gray-700" />
                  </div>
                  <div className="mt-4 grid grid-cols-1 gap-3 sm:grid-cols-2">
                    <button
onClick={async () => { const r = await loginWithGoogle(); if (r.success) navigate('/?from=login', { replace: true }); }}
                      className="w-full inline-flex items-center justify-center gap-2 py-2.5 bg-white dark:bg-gray-900 border border-gray-300 dark:border-gray-700 rounded-xl text-gray-700 dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-800"
                    >
                      <img src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg" alt="" className="h-5 w-5" />
                      <span>Google</span>
                    </button>
                    <button
onClick={async () => { const r = await loginWithFacebook(); if (r.success) navigate('/?from=login', { replace: true }); }}
                      className="w-full inline-flex items-center justify-center gap-2 py-2.5 bg-white dark:bg-gray-900 border border-gray-300 dark:border-gray-700 rounded-xl text-gray-700 dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-800"
                    >
                      <img src="https://www.svgrepo.com/show/452196/facebook-1.svg" alt="" className="h-5 w-5" />
                      <span>Facebook</span>
                    </button>
                  </div>
                </div>

                <p className="mt-6 text-center text-sm text-gray-600 dark:text-gray-300">
                  New user?{' '}
                  <Link className="text-ayurveda-600 dark:text-ayurveda-400 font-medium hover:underline" to="/register">Create an account</Link>
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
                <h2 className="text-3xl font-bold font-serif">Holistic Wellness, Powered by AI</h2>
                <p className="mt-3 text-ayurveda-100">Access personalized dosha analysis, symptom checking, and Ayurvedic recommendations.</p>
                <ul className="mt-8 space-y-3 text-ayurveda-50">
                  <li className="flex items-start gap-3"><span className="mt-1">•</span> Secure authentication keeps your health data private</li>
                  <li className="flex items-start gap-3"><span className="mt-1">•</span> Continue where you left off across modules</li>
                  <li className="flex items-start gap-3"><span className="mt-1">•</span> Beautiful, calming UI designed for focus</li>
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

export default Login;
