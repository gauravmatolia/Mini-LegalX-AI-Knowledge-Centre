import React, { useEffect, useState } from 'react';
import { fetchTopicById } from '../services/api';
import AIAssistant from './AIAssistant';

export default function LegalDetail({ topicId }) {
  const [topic, setTopic] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchTopicById(topicId)
      .then(res => {
        setTopic(res.data);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setError("Failed to load topic details");
        setLoading(false);
      });
  }, [topicId]);

  const parseTextToList = (text) => {
    if (!text) return [];
    return text
      .split(/[\n•\-\*]/g)
      .map(item => item.trim())
      .filter(item => item.length > 0);
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center py-20">
        <div className="text-center">
          <div className="inline-block">
            <div className="w-12 h-12 border-4 border-yellow-600 border-t-yellow-300 rounded-full animate-spin mb-4"></div>
          </div>
          <p className="text-gray-300 font-medium">Retrieving detailed information...</p>
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

  if (!topic) {
    return <div className="text-center py-10 text-red-400 font-medium">Topic details not found.</div>;
  }

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 items-start">
      {/* Information Column (Left/Center) */}
      <div className="lg:col-span-2 space-y-6">
        {/* Title Header */}
        <div className="bg-gradient-to-r from-gray-900 to-black border-2 border-yellow-600 rounded-lg p-8">
          <h2 className="text-3xl font-bold text-white mb-2">{topic.name}</h2>
          <p className="text-gray-300 text-lg">{topic.shortDescription}</p>
        </div>

        {/* Summary Section */}
        <div className="bg-gradient-to-r from-gray-900 to-black border-2 border-yellow-600 rounded-lg p-6">
          <h3 className="text-lg font-bold text-yellow-400 border-b-2 border-yellow-600 pb-3 mb-4">
            Overview & Summary
          </h3>
          <p className="text-gray-200 leading-relaxed text-base">{topic.summary}</p>
        </div>

        {/* Information Extraction Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Key Rights */}
          <div className="bg-gradient-to-br from-gray-900 to-black border-2 border-yellow-600 rounded-lg p-5 hover:shadow-lg hover:shadow-yellow-600/30 transition">
            <h4 className="font-bold text-yellow-400 mb-3 text-lg">
              Key Rights
            </h4>
            <div className="space-y-2">
              {parseTextToList(topic.keyRights).length > 0 ? (
                parseTextToList(topic.keyRights).map((item, idx) => (
                  <div key={idx} className="flex gap-3">
                    <span className="text-yellow-500 font-bold">+</span>
                    <p className="text-sm text-gray-200">{item}</p>
                  </div>
                ))
              ) : (
                <p className="text-sm text-gray-400 italic">{topic.keyRights}</p>
              )}
            </div>
          </div>

          {/* Important Provisions */}
          <div className="bg-gradient-to-br from-gray-900 to-black border-2 border-yellow-600 rounded-lg p-5 hover:shadow-lg hover:shadow-yellow-600/30 transition">
            <h4 className="font-bold text-yellow-400 mb-3 text-lg">
              Important Provisions
            </h4>
            <div className="space-y-2">
              {parseTextToList(topic.importantProvisions).length > 0 ? (
                parseTextToList(topic.importantProvisions).map((item, idx) => (
                  <div key={idx} className="flex gap-3">
                    <span className="text-yellow-500 font-bold">•</span>
                    <p className="text-sm text-gray-200">{item}</p>
                  </div>
                ))
              ) : (
                <p className="text-sm text-gray-400 italic">{topic.importantProvisions}</p>
              )}
            </div>
          </div>

          {/* Important Penalties */}
          <div className="bg-gradient-to-br from-gray-900 to-black border-2 border-yellow-600 rounded-lg p-5 hover:shadow-lg hover:shadow-yellow-600/30 transition">
            <h4 className="font-bold text-yellow-400 mb-3 text-lg">
              Important Penalties
            </h4>
            <div className="space-y-2">
              {parseTextToList(topic.importantPenalties).length > 0 ? (
                parseTextToList(topic.importantPenalties).map((item, idx) => (
                  <div key={idx} className="flex gap-3">
                    <span className="text-yellow-500 font-bold">!</span>
                    <p className="text-sm text-gray-200">{item}</p>
                  </div>
                ))
              ) : (
                <p className="text-sm text-gray-400 italic">{topic.importantPenalties}</p>
              )}
            </div>
          </div>

          {/* Who Can Benefit */}
          <div className="bg-gradient-to-br from-gray-900 to-black border-2 border-yellow-600 rounded-lg p-5 hover:shadow-lg hover:shadow-yellow-600/30 transition">
            <h4 className="font-bold text-yellow-400 mb-3 text-lg">
              Who Can Benefit
            </h4>
            <div className="space-y-2">
              {parseTextToList(topic.whoCanBenefit).length > 0 ? (
                parseTextToList(topic.whoCanBenefit).map((item, idx) => (
                  <div key={idx} className="flex gap-3">
                    <span className="text-yellow-500 font-bold">→</span>
                    <p className="text-sm text-gray-200">{item}</p>
                  </div>
                ))
              ) : (
                <p className="text-sm text-gray-400 italic">{topic.whoCanBenefit}</p>
              )}
            </div>
          </div>
        </div>

        {/* Web Context */}
        {topic.webContext && (
          <div className="bg-gradient-to-r from-gray-900 to-black border-2 border-yellow-600 rounded-lg p-6">
            <h4 className="font-bold text-yellow-400 mb-3 text-lg">
              Real-World Context & Updates
            </h4>
            <p className="text-gray-200 leading-relaxed text-sm">{topic.webContext}</p>
          </div>
        )}
      </div>

      {/* Interactive Assistant (Right Panel) */}
      <div className="lg:col-span-1 sticky top-24">
        <AIAssistant topicName={topic.name} />
      </div>
    </div>
  );
}