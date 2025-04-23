import React, { useState, useEffect, useContext } from 'react';
import { AuthContext } from '../components/AuthProvider';

const ResultPage = () => {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(true);
  const { user } = useContext(AuthContext);

  useEffect(() => {
    const fetchResult = async () => {
      try {
        const token = await user.getIdToken();
        const response = await fetch('http://localhost:8080/api/results/latest', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        if (response.ok) {
          const data = await response.json();
          setResult(data);
        } else {
          console.error('Fetch error:', response.statusText);
        }
      } catch (error) {
        console.error("Fetch error:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchResult();
  }, [user]);

  if (loading) return <div className="flex justify-center items-center h-screen">Loading...</div>;

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <div className="max-w-4xl mx-auto bg-white p-8 rounded-lg shadow-md">
        <h1 className="text-2xl font-bold mb-6">Analysis Result</h1>
        {result ? (
          <div className="space-y-6">
            <p className="text-lg">{result.textData || "No text data available"}</p>
            {result.resultImage1 && (
              <img src={result.resultImage1} alt="Result 1" className="w-full rounded-lg" />
            )}
            {result.resultImage2 && (
              <img src={result.resultImage2} alt="Result 2" className="w-full rounded-lg" />
            )}
          </div>
        ) : (
          <p>No results found</p>
        )}
      </div>
    </div>
  );
};

export default ResultPage;