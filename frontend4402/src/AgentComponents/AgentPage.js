import React, { useState } from "react";
import axios from "axios";
import AgentDashboard from "./AgentDashboard";

const AgentPage = () => {
  const [agentID, setAgentID] = useState("");
  const [loggedInAgent, setLoggedInAgent] = useState({});
  const [loggedIn, setLoggedIn] = useState(false);

  const API_BASE_URL = "https://5pq8iah053.execute-api.us-east-1.amazonaws.com/dev/api";

  const handleIDChange = (e) => {
    setAgentID(e.target.value);
  };

  const handleGetAgent = async () => {
    try {
        if (!agentID || agentID.trim() === '') {
            alert('Please enter an Agent ID');
            return;
        }

        console.log('Calling API with agentId:', agentID.trim());
        
        const response = await axios.post(`${API_BASE_URL}/getAgent`, {
            agentId: agentID.trim()
        });
        
        if (!response.data) {
            throw new Error('No data received from server');
        }

        // Transform the response data to match expected format
        const transformedData = {
            FIRST_NAME: response.data.firstName,
            LAST_NAME: response.data.lastName,
            EMAIL: response.data.email,
            PHONE: response.data.phone,
            LICENSE_NUMBER: response.data.licenseNumber,
            AGENT_ID: response.data.agentId
        };

        setLoggedInAgent(transformedData);
        setLoggedIn(true);
    } catch (error) {
        console.error('API Error:', error);
        const errorMessage = error.response?.data?.message 
            || error.response?.data?.error
            || error.message 
            || 'Failed to retrieve agent information';
        alert(`Error: ${errorMessage}`);
    }
};

  if (!loggedIn) {
    return (
      <div style={styles.container}>
        <h2 style={styles.title}>Enter Agent ID</h2>
        <input
          type="text"
          name="agentID"
          placeholder="Agent ID"
          style={styles.input}
          onChange={handleIDChange}
        />
        <button style={styles.button} onClick={handleGetAgent}>
          View Information
        </button>
        <h3>The following Agent IDs are pre-populated: 1, 2</h3>
      </div>
    );
  } else {
    return (
      <>
      <AgentDashboard agent={loggedInAgent} />
      </>
    );
  }
};

const styles = {
  container: {
    maxWidth: "600px",
    margin: "auto",
    padding: "20px",
    fontFamily: "Arial, sans-serif",
  },
  title: {
    textAlign: "center",
    fontSize: "24px",
    marginBottom: "20px",
  },
  formContainer: {
    display: "flex",
    flexDirection: "column",
  },
  inputContainer: {
    marginBottom: "15px",
  },
  input: {
    width: "100%",
    padding: "10px",
    marginBottom: "10px",
    fontSize: "16px",
    border: "1px solid #ccc",
    borderRadius: "5px",
  },
  button: {
    width: "100%",
    padding: "10px",
    fontSize: "18px",
    backgroundColor: "#4CAF50",
    color: "white",
    border: "none",
    borderRadius: "5px",
    cursor: "pointer",
  },
};

export default AgentPage;
