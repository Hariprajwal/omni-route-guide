const axios = require('axios');

// OmniRoute Local Server Endpoint
const API_URL = 'http://localhost:20128/v1/chat/completions';

// Headers: OmniRoute mimics OpenAI, so we pass a dummy Bearer token
const headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Bearer dummy-key'
};

// Payload
const data = {
  model: 'felo/auto', // Explicitly use the free keyless Felo provider
  stream: false,      // Set to true if you want a streaming response
  messages: [
    { role: 'user', content: 'Hello! What can you do?' }
  ]
};

console.log('Sending request to OmniRoute...');

axios.post(API_URL, data, { headers })
  .then(response => {
    console.log('\n--- Response ---');
    console.log(response.data.choices[0].message.content);
  })
  .catch(error => {
    console.error('Error:', error.message);
    if (error.response) {
      console.error('Server replied:', error.response.data);
    }
  });
