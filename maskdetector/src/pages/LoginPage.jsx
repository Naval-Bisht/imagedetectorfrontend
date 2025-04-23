import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { auth } from '../firebase';
import { GoogleAuthProvider, signInWithPopup } from 'firebase/auth';
import { Header } from './Header';
import { Footer } from './Footer';
const LoginPage = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const from = location.state?.from?.pathname || "/dashboard";
  const [showLoginBT,setShowLoginBT] = useState(true)

  const handleGoogleLogin = async () => {
    try {
      const provider = new GoogleAuthProvider();
      await signInWithPopup(auth, provider);
      navigate(from, { replace: true });
    } catch (error) {
      console.error("Login error:", error);
    }
  };

  return (
    <>
    <Header   loginBT={showLoginBT}  />
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="bg-white p-8 rounded-lg shadow-md">
        <h1 className="text-2xl font-bold mb-6 text-center">Login</h1>
        <button
          onClick={handleGoogleLogin}
          className="w-full bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 flex items-center justify-center gap-2"
        >
          <svg className="w-5 h-5" viewBox="0 0 24 24">
            <path fill="currentColor" d="M12.24 10.4V14h-1v-4h2.24l2.26-2.26-1.42-1.42-2.84 2.84zm3.76 0l2.26-2.26-1.42-1.42-2.84 2.84V10.4h1zm-4-4.8V8h1V5.6l-2.26-2.26-1.42 1.42 2.84 2.84zm-4.8 4.8l-2.26 2.26 1.42 1.42 2.84-2.84V10.4h-1zm0-4.8l-2.26 2.26 1.42 1.42 2.84-2.84V5.6h-1zm4.8 12.8V15.6h-1v4h2.24l2.26 2.26 1.42-1.42-2.84-2.84zm3.76 0l2.26 2.26 1.42-1.42-2.84-2.84V15.6h-1z"/>
          </svg>
          Sign in with Google
        </button>
      </div>
    </div>
    <Footer />
    </>
  );
};

export default LoginPage;