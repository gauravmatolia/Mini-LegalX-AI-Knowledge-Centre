import React, { useState, useRef, useEffect } from 'react';
import { sendChatMessage } from '../services/api';

export default function AIAssistant({ topicName = 'Legal Documents' }) {
  const [messages, setMessages] = useState([
    { sender: 'ai', text: `Welcome to Legal Assistant. I can help you understand legal concepts and regulations. How can I assist you today?` }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMsg = input.trim();
    setInput('');
    setMessages(prev => [...prev, { sender: 'user', text: userMsg }]);
    setLoading(true);

    try {
      const response = await sendChatMessage(userMsg);
      
      if (response.data.success) {
        setMessages(prev => [...prev, { sender: 'ai', text: response.data.reply }]);
      } else {
        setMessages(prev => [...prev, { sender: 'ai', text: 'Sorry, I encountered an error processing your request. Please try again.' }]);
      }
    } catch (err) {
      console.error(err);
      setMessages(prev => [...prev, { sender: 'ai', text: 'I encountered a network error. Please check your connection and try again.' }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-black border-2 border-yellow-600 text-white rounded-lg flex flex-col h-[600px] overflow-hidden shadow-lg shadow-yellow-600/30">
      {/* Bot Header */}
      <div className="bg-gradient-to-r from-black to-gray-900 px-6 py-4 border-b-2 border-yellow-600">
        <div className="flex items-center justify-between">
          <span className="font-bold text-sm tracking-wider text-white">LEGAL ASSISTANT</span>
          <span className="text-xs text-yellow-400 font-mono">Online</span>
        </div>
      </div>

      {/* Message Output Thread */}
      <div className="flex-1 overflow-y-auto p-5 space-y-4">
        {messages.map((msg, index) => (
          <div key={index} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[75%] rounded-lg p-4 text-sm leading-relaxed ${
              msg.sender === 'user' 
                ? 'bg-yellow-600 text-black rounded-br-none shadow-lg shadow-yellow-600/50' 
                : 'bg-gray-800 text-gray-100 rounded-bl-none border border-yellow-600'
            }`}>
              {msg.text}
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex justify-start">
            <div className="bg-gray-800 border border-yellow-600 rounded-lg rounded-bl-none p-4 text-sm text-gray-300 flex items-center gap-2">
              Thinking<span className="animate-bounce">.</span><span className="animate-bounce [animation-delay:0.2s]">.</span><span className="animate-bounce [animation-delay:0.4s]">.</span>
            </div>
          </div>
        )}
        <div ref={chatEndRef} />
      </div>

      {/* Input Section */}
      <div className="p-4 bg-gray-900 border-t-2 border-yellow-600">
        <form onSubmit={handleSendMessage} className="flex gap-2">
          <input 
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask a legal question..."
            className="flex-1 bg-gray-800 text-white placeholder-gray-500 rounded px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-yellow-600 border border-gray-700 transition"
            disabled={loading}
          />
          <button 
            type="submit"
            className="bg-yellow-600 hover:bg-yellow-500 text-black font-bold text-sm px-6 py-2 rounded transition duration-300 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg hover:shadow-yellow-600/50"
            disabled={loading || !input.trim()}
          >
            Send
          </button>
        </form>
        <p className="text-xs text-gray-500 mt-2">Ask questions about legal documents, regulations, rights, and obligations.</p>
      </div>
    </div>
  );
}