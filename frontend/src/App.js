import React, { useState } from 'react';
import TopicCards from './components/TopicCards';
import LegalDetail from './components/LegalDetail';
import AIAssistant from './components/AIAssistant';

function App() {
  const [currentPage, setCurrentPage] = useState('home'); // 'home', 'assistant', 'detail'
  const [selectedTopicId, setSelectedTopicId] = useState(null);

  const handleSelectTopic = (topicId) => {
    setSelectedTopicId(topicId);
    setCurrentPage('detail');
  };

  const handleBackToHome = () => {
    setCurrentPage('home');
    setSelectedTopicId(null);
  };

  const handleNavigateToAssistant = () => {
    setCurrentPage('assistant');
  };

  return (
    <div className="min-h-screen bg-black text-white font-sans">
      {/* Header with Navigation */}
      <header className="bg-gradient-to-r from-black via-gray-900 to-black border-b-2 border-yellow-600 shadow-lg py-6 px-6 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <h1 
            className="text-3xl font-bold tracking-wider cursor-pointer hover:text-yellow-400 transition duration-300"
            onClick={handleBackToHome}
          >
            LEGALX
          </h1>
          <nav className="flex gap-6">
            <button 
              onClick={handleBackToHome}
              className={`px-6 py-2 rounded font-semibold text-sm transition duration-300 ${
                currentPage === 'home' 
                  ? 'bg-yellow-600 text-black' 
                  : 'text-white hover:text-yellow-400 border-2 border-yellow-600'
              }`}
            >
              Home
            </button>
            <button 
              onClick={handleNavigateToAssistant}
              className={`px-6 py-2 rounded font-semibold text-sm transition duration-300 ${
                currentPage === 'assistant' 
                  ? 'bg-yellow-600 text-black' 
                  : 'text-white hover:text-yellow-400 border-2 border-yellow-600'
              }`}
            >
              Legal Assistant
            </button>
          </nav>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="max-w-7xl mx-auto px-4 py-12">
        {/* Home Page - Display Topics */}
        {currentPage === 'home' && (
          <div>
            <div className="mb-12 text-center">
              <h2 className="text-4xl font-bold text-white mb-4">Legal Topics & Acts</h2>
              <p className="text-gray-300 text-lg">Explore comprehensive legal information and regulations</p>
            </div>
            <TopicCards onSelectTopic={handleSelectTopic} />
          </div>
        )}

        {/* Detail Page - Show Topic Details + Chat */}
        {currentPage === 'detail' && selectedTopicId && (
          <div>
            <button 
              onClick={handleBackToHome}
              className="mb-8 text-yellow-400 hover:text-yellow-300 font-semibold text-sm transition duration-300"
            >
              ← Back to Topics
            </button>
            <LegalDetail topicId={selectedTopicId} />
          </div>
        )}

        {/* Legal Assistant Page - Standalone Chat */}
        {currentPage === 'assistant' && (
          <div>
            <div className="mb-12">
              <h2 className="text-4xl font-bold text-white mb-4">Legal Assistant</h2>
              <p className="text-gray-300 text-lg">Ask questions about legal documents and regulations</p>
            </div>
            <div className="flex justify-center">
              <div className="w-full max-w-2xl">
                <AIAssistant topicName="Legal Documents" />
              </div>
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-gradient-to-r from-black via-gray-900 to-black border-t-2 border-yellow-600 text-gray-400 py-6 px-4 mt-16">
        <div className="max-w-7xl mx-auto text-center text-sm">
          <p>LEGALX - Powered by AI Agents</p>
          <p>Made By - Gaurav Matolia</p>
        </div>
      </footer>
    </div>
  );
}

export default App;