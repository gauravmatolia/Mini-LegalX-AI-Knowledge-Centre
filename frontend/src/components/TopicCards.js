import React, { useEffect, useState } from 'react';
import { fetchTopics } from '../services/api';

export default function TopicCards({ onSelectTopic }) {
  const [topics, setTopics] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchTopics()
      .then(res => {
        setTopics(res.data || []);
        setLoading(false);
      })
      .catch(err => {
        console.error("Error fetching topics:", err);
        setError("Failed to load legal topics. Please try again later.");
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="flex justify-center items-center py-20">
        <div className="text-center">
          <div className="inline-block">
            <div className="w-12 h-12 border-4 border-yellow-600 border-t-yellow-300 rounded-full animate-spin mb-4"></div>
          </div>
          <p className="text-gray-300 font-medium">Processing legal documents...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-10 bg-red-900 bg-opacity-30 border-2 border-red-600 rounded-lg p-4">
        <p className="text-red-300 font-medium">{error}</p>
      </div>
    );
  }

  if (!topics || topics.length === 0) {
    return (
      <div className="text-center py-10 bg-yellow-900 bg-opacity-20 border-2 border-yellow-600 rounded-lg p-4">
        <p className="text-yellow-300 font-medium">No legal topics found. Please ensure PDF documents are in the legal_documents folder.</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {topics.map((topic) => (
        <div 
          key={topic._id} 
          className="bg-gradient-to-br from-gray-900 to-black border-2 border-yellow-600 rounded-lg p-6 flex flex-col justify-between hover:shadow-2xl hover:shadow-yellow-600/50 transition-all duration-300 cursor-pointer group"
        >
          <div>
            <h3 className="text-xl font-bold text-white group-hover:text-yellow-400 transition-colors mb-3">
              {topic.name || 'Legal Topic'}
            </h3>
            <p className="text-gray-300 text-sm line-clamp-3 mb-4">
              {topic.shortDescription || 'Legal information about this topic'}
            </p>
          </div>
          <button 
            onClick={() => onSelectTopic(topic._id)}
            className="w-full bg-yellow-600 hover:bg-yellow-500 text-black text-sm font-bold py-3 px-4 rounded transition duration-300 shadow-lg hover:shadow-yellow-600/50"
          >
            Read More
          </button>
        </div>
      ))}
    </div>
  );
}