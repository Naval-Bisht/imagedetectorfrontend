import React, { useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { AuthContext } from '../components/AuthProvider';

const UploadPage = () => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const navigate = useNavigate();
  const { user } = useContext(AuthContext);

  const handleFileChange = (e) => {
    if (e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    setUploading(true);
    try {
      const token = await user.getIdToken();
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch('http://localhost:8080/api/upload', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        },
        body: formData
      });

      if (response.status === 200) {
        navigate(`/result/${Date.now()}`);
      } else {
        console.error('Upload failed:', response.statusText);
      }
    } catch (error) {
      console.error("Upload error:", error);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-md">
        <h1 className="text-2xl font-bold mb-6">Upload Image</h1>
        <input
          type="file"
          accept="image/*"
          onChange={handleFileChange}
          className="mb-4 w-full"
        />
        <button
          onClick={handleUpload}
          disabled={!file || uploading}
          className="w-full bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 disabled:bg-gray-400"
        >
          {uploading ? "Uploading..." : "Upload"}
        </button>
      </div>
    </div>
  );
};

export default UploadPage;