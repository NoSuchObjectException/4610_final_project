import React, { useState } from 'react';
import axios from 'axios';
import ClientDashboard from './ClientDashboard';

const ClientPage = () => {
  const [clientID, setClientID] = useState('');
  const [loggedInClient, setLoggedInClient] = useState({});
  const [loggedIn, setLoggedIn] = useState(false);

  const API_BASE_URL = "https://5pq8iah053.execute-api.us-east-1.amazonaws.com/dev/api";

  const handleIDChange = (e) => {
    setClientID(e.target.value);
  };

  const handleGetClient = async () => {
    try {
      if (!clientID || clientID.trim() === '') {
        alert('Please enter a Client ID');
        return;
      }

      console.log('Calling API with clientId:', clientID.trim());
      
      const response = await axios.post(`${API_BASE_URL}/getClient`, {
        action: 'get_client',  // Add this line
        clientId: clientID.trim()
      }, {
        headers: {
          'Content-Type': 'application/json',
        }
      });

      console.log('Raw response:', response.data);
      
      if (!response.data) {
        throw new Error('No data received from server');
      }

      setLoggedInClient(response.data);
      setLoggedIn(true);
    } catch (error) {
      console.error('Error getting client:', error);
      const errorMessage = error.response?.data?.message 
        || error.message 
        || 'Failed to retrieve client information';
      alert(`Error: ${errorMessage}`);
    }
  };

  if (!loggedIn) {
    return (
      <div style={styles.container}>
        <h2 style={styles.title}>Enter Client ID</h2>
        <input 
          type="text" 
          name="clientID" 
          placeholder="Client ID" 
          style={styles.input} 
          onChange={handleIDChange} 
        />
        <button style={styles.button} onClick={handleGetClient}>
          View Information
        </button>
        <h3>The following Client IDs are pre-populated: 1, 2</h3>
      </div>
    );
  } else {
    return (
      <ClientDashboard client={loggedInClient} />
    );
  }
};

const styles = {
  container: {
    maxWidth: '600px',
    margin: 'auto',
    padding: '20px',
    fontFamily: 'Arial, sans-serif',
  },
  title: {
    textAlign: 'center',
    fontSize: '24px',
    marginBottom: '20px',
  },
  formContainer: {
    display: 'flex',
    flexDirection: 'column',
  },
  inputContainer: {
    marginBottom: '15px',
  },
  input: {
    width: '100%',
    padding: '10px',
    marginBottom: '10px',
    fontSize: '16px',
    border: '1px solid #ccc',
    borderRadius: '5px',
  },
  button: {
    width: '100%',
    padding: '10px',
    fontSize: '18px',
    backgroundColor: '#4CAF50',
    color: 'white',
    border: 'none',
    borderRadius: '5px',
    cursor: 'pointer',
  },
};

export default ClientPage;