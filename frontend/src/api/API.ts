import axios from 'axios';

// Create an instance of Axios with default configuration
const instance = axios.create({
  baseURL: 'http://localhost:8000', // Replace with your API base URL
  timeout: 5000, // Request timeout in milliseconds
  headers: {
    'Content-Type': 'application/json',
  },
});

export default instance;
