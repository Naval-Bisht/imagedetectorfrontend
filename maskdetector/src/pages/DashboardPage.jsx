import React from 'react';
import { useNavigate } from 'react-router-dom';
import { auth } from '../firebase';
import { signOut } from 'firebase/auth';

const DashboardPage = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <div className="max-w-7xl mx-auto">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-3xl font-bold">Dashboard</h1>
          <button
            onClick={() => signOut(auth)}
            className="bg-red-500 text-white py-2 px-4 rounded hover:bg-red-600"
          >
            Logout
          </button>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-white p-6 rounded-lg shadow-md">
            <div className="flex flex-col gap-4">
              <button
                onClick={() => navigate("/upload")}
                className="bg-green-500 text-white py-2 px-4 rounded hover:bg-green-600"
              >
                Upload Image
              </button>
              <button
                onClick={() => navigate("/history")}
                className="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600"
              >
                View Past Results
              </button>
            </div>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h2 className="text-xl font-semibold mb-4">Analytics Views</h2>
            <div className="h-64 bg-gray-200 flex items-center justify-center">
              <p className="text-gray-500">ELK Analytics Placeholder</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;