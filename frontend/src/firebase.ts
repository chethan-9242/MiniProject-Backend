import { initializeApp } from 'firebase/app';
import { getAuth, GoogleAuthProvider, FacebookAuthProvider } from 'firebase/auth';

// Use env vars if present; otherwise fall back to your provided config so dev works immediately
const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY || 'AIzaSyBGtReR9iBtWYH6l8gNNlk78wXmXQfBhT0',
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN || 'swasthvedha.firebaseapp.com',
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID || 'swasthvedha',
  appId: import.meta.env.VITE_FIREBASE_APP_ID || '1:1014438785332:web:3a0403041d045c99493561',
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
export const googleProvider = new GoogleAuthProvider();
googleProvider.setCustomParameters({ prompt: 'select_account' });
export const facebookProvider = new FacebookAuthProvider();
facebookProvider.addScope('email');
