import React, { useState, useEffect, useContext } from 'react';
import { AuthContext } from '../components/AuthProvider';
import { Header } from './Header';
import { Footer } from './Footer';
const HistoryPage = () => {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const { user } = useContext(AuthContext);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const token = await user.getIdToken();
        const response = await fetch('http://localhost:8080/api/results/history', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        if (response.ok) {
          const data = await response.json();
          setHistory(data);
        } else {
          console.error('Fetch error:', response.statusText);
        }
      } catch (error) {
        console.error("Fetch error:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchHistory();
  }, [user]);

  if (loading) return <div className="flex justify-center items-center h-screen">Loading...</div>;

  return ( <>
    <Header />
    <div className="min-h-screen bg-gray-100 p-6">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-2xl font-bold mb-6">Search History</h1>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {history.length > 0 ? (
            history.map(item => (
              <div key={item.id} className="bg-white p-4 rounded-lg shadow-md">
                <img src={item.imageUrl} alt="Search" className="w-full h-48 object-cover rounded" />
                <p className="mt-2 text-sm text-gray-600">
                  {new Date(item.createdAt).toLocaleString()}
                </p>
              </div>
            ))
          ) : (
            <p>No previous searches found</p>
          )}
        </div>
      </div>
    </div><Footer />
    </>
  );
};

export default HistoryPage;