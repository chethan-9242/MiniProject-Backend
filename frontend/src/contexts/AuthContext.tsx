import React, { createContext, useContext, useEffect, useState } from 'react';
import { signInWithPopup, signInWithRedirect, getRedirectResult, onAuthStateChanged, getIdToken, createUserWithEmailAndPassword, signInWithEmailAndPassword, updateProfile } from 'firebase/auth';
import { auth as fbAuth, googleProvider, facebookProvider } from '../firebase';

interface User {
  id: string;
  email: string;
  name: string;
  dateJoined: string;
}

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<{ success: boolean; message?: string }>;
  register: (name: string, email: string, password: string) => Promise<{ success: boolean; message?: string }>;
  loginWithGoogle: () => Promise<{ success: boolean; message?: string }>;
  loginWithFacebook: () => Promise<{ success: boolean; message?: string }>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: React.ReactNode;
}

const API_URL = (process.env.REACT_APP_API_URL || 'http://localhost:8000').replace(/\/$/, '');
const AUTH_MODE = (process.env.REACT_APP_AUTH_MODE || 'firebase') as 'firebase' | 'backend';


export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

useEffect(() => {
    if (AUTH_MODE === 'backend') {
      checkAuthState();
    } else {
      // Frontend-only mode: rely on Firebase auth state
      const unsub = onAuthStateChanged(fbAuth, async (fbUser) => {
        try {
          if (fbUser) {
            const idToken = await getIdToken(fbUser, true);
            localStorage.setItem('swasthvedha_token', idToken);
            const existing = localStorage.getItem('swasthvedha_user');
            let localUser: User | null = existing ? JSON.parse(existing) : null;
            const hydrated: User = {
              id: fbUser.uid,
              email: fbUser.email || (localUser?.email || ''),
              name: fbUser.displayName || (localUser?.name || 'User'),
              dateJoined: (fbUser.metadata && (fbUser.metadata as any).creationTime) || localUser?.dateJoined || new Date().toISOString(),
            };
            localStorage.setItem('swasthvedha_user', JSON.stringify(hydrated));
            setUser(hydrated);
          } else {
            localStorage.removeItem('swasthvedha_token');
            localStorage.removeItem('swasthvedha_user');
            setUser(null);
          }
        } finally {
          setIsLoading(false);
        }
      });
      // Process redirect results if any (no-op; onAuthStateChanged will reflect sign-in)
      getRedirectResult(fbAuth).catch(() => {});
      return () => unsub();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const checkAuthState = async () => {
    try {
      const token = localStorage.getItem('swasthvedha_token');
      if (!token) {
        setIsLoading(false);
        return;
      }
      const res = await fetch(`${API_URL}/api/auth/me`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (res.ok) {
        const me = await res.json();
        setUser(me);
      } else {
        localStorage.removeItem('swasthvedha_token');
        setUser(null);
      }
    } catch (e) {
      setUser(null);
    } finally {
      setIsLoading(false);
    }
  };

const register = async (name: string, email: string, password: string) => {
    setIsLoading(true);
    try {
      // Always use Firebase for email/password registration to avoid CORS/backend dependency
      const cred = await createUserWithEmailAndPassword(fbAuth, email, password);
      try {
        await updateProfile(cred.user, { displayName: name });
      } catch {}
      // Desired UX: after registration, user should NOT be signed in; show login next
      try { localStorage.removeItem('swasthvedha_after_login'); } catch {}
      try { await fbAuth.signOut(); } catch {}
      return { success: true, message: 'Registration successful! Please login.' };
    } catch (e) {
      return { success: false, message: 'Registration failed. Please try again.' };
    } finally {
      setIsLoading(false);
    }
  };

const login = async (email: string, password: string) => {
    setIsLoading(true);
    try {
      // Always use Firebase for email/password login to avoid CORS/backend dependency
      const cred = await signInWithEmailAndPassword(fbAuth, email, password);
      const idToken = await getIdToken(cred.user, true);
      const local = {
        id: cred.user.uid,
        email: cred.user.email || '',
        name: cred.user.displayName || 'User',
        dateJoined: (cred.user.metadata && (cred.user.metadata as any).creationTime) || new Date().toISOString(),
      };
      localStorage.setItem('swasthvedha_token', idToken);
      localStorage.setItem('swasthvedha_user', JSON.stringify(local));
      setUser(local);
      return { success: true };
    } catch (e) {
      return { success: false, message: 'Login failed. Please try again.' };
    } finally {
      setIsLoading(false);
    }
  };

  // Firebase-only flow (no backend required)
const loginWithFirebaseProvider = async (provider: 'google' | 'facebook') => {
    setIsLoading(true);
    try {
      const providerObj = provider === 'google' ? googleProvider : facebookProvider;

      // Prefer redirect for Facebook and mobile/Safari to avoid popup issues
      const ua = (typeof navigator !== 'undefined' ? navigator.userAgent : '').toLowerCase();
      const isIOS = /iphone|ipad|ipod/.test(ua);
      const isAndroid = /android/.test(ua);
      const isMobile = isIOS || isAndroid;
      const isSafari = /^((?!chrome|android).)*safari\//.test(ua);

if (provider === 'facebook' || isMobile || isSafari) {
        try { localStorage.setItem('swasthvedha_after_login', '1'); } catch {}
        await signInWithRedirect(fbAuth, providerObj);
        return { success: true };
      }

      try {
        const cred = await signInWithPopup(fbAuth, providerObj);
        // Create user object directly from Firebase user data
        const user = {
          id: cred.user.uid,
          email: cred.user.email || '',
          name: cred.user.displayName || 'User',
          dateJoined: new Date().toISOString()
        };
        // Store user data and token locally
        const idToken = await getIdToken(cred.user, true);
        localStorage.setItem('swasthvedha_token', idToken);
        localStorage.setItem('swasthvedha_user', JSON.stringify(user));
setUser(user);
        try { localStorage.setItem('swasthvedha_after_login', '1'); } catch {}
        return { success: true };
      } catch (e: any) {
        // Fallback to redirect if popups are blocked or unsupported
if (e?.code === 'auth/popup-blocked' || e?.code === 'auth/operation-not-supported-in-this-environment') {
          try { localStorage.setItem('swasthvedha_after_login', '1'); } catch {}
          await signInWithRedirect(fbAuth, providerObj);
          return { success: true };
        }
        throw e;
      }
    } catch (e: any) {
      console.error('Firebase sign-in error:', e);
      return { success: false, message: e?.message || 'Sign-in failed. Please try again.' };
    } finally {
      setIsLoading(false);
    }
  };

  const loginWithGoogle = () => loginWithFirebaseProvider('google');
  const loginWithFacebook = () => loginWithFirebaseProvider('facebook');

const logout = async () => {
    try { await fbAuth.signOut(); } catch {}
    localStorage.removeItem('swasthvedha_token');
    localStorage.removeItem('swasthvedha_user');
    setUser(null);
  };

  const value = {
    user,
    isAuthenticated: !!user,
    isLoading,
    login,
    register,
    loginWithGoogle,
    loginWithFacebook,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
