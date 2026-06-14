import axios from 'axios';

const API_BASE_URL = 'http://localhost:5001/api'; // Backend API endpoint (port 5001 to avoid AirPlay conflict on macOS)

// Topics endpoints
export const fetchTopics = () => axios.get(`${API_BASE_URL}/topics`);
export const fetchTopicById = (id) => axios.get(`${API_BASE_URL}/topic/${id}`);

// Chat endpoint
export const sendChatMessage = (message) => 
    axios.post(`${API_BASE_URL}/chat`, { message });

// Health check
export const checkHealth = () => axios.get(`${API_BASE_URL}/health`);