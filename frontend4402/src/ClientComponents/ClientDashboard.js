import React, { useState, useEffect } from "react";
import ClientPropertyContainer from "./ClientPropertyContainer";
import axios from "axios";

const ClientDashboard = ({ client }) => {
  const [agents, setAgents] = useState([]);
  const [transactions, setTransactions] = useState([]);
  const [appointments, setAppointments] = useState([]);

  const API_BASE_URL = "https://acyx49drq5.execute-api.us-east-1.amazonaws.com/dev/api";

  const {
    firstName: FIRST_NAME,
    lastName: LAST_NAME,
    email: EMAIL,
    phone: PHONE,
    street: STREET,
    city: CITY,
    state: STATE,
    zipcode: ZIPCODE,
    clientId: CLIENT_ID,
  } = client;

  useEffect(() => {
    if (CLIENT_ID) {
      fetchAppointments();
      fetchTransactions();
      fetchAgents();
    }
  }, [CLIENT_ID]);

  const fetchAppointments = async () => {
    try {
      const response = await axios.post(`${API_BASE_URL}/getClientAppointments`, {
        action: 'get_appointments',
        clientId: CLIENT_ID
      });
      setAppointments(response.data || []);
    } catch (error) {
      console.error('Error fetching appointments:', error);
      setAppointments([]);
    }
  };

  const fetchTransactions = async () => {
    try {
      const response = await axios.post(`${API_BASE_URL}/getClientTransactions`, {
        action: 'get_transactions',
        clientId: CLIENT_ID
      });
      setTransactions(response.data || []);
    } catch (error) {
      console.error('Error fetching transactions:', error);
      setTransactions([]);
    }
  };

  const fetchAgents = async () => {
    try {
      const response = await axios.post(`${API_BASE_URL}/getClientAgents`, {
        action: 'get_agents',
        clientId: CLIENT_ID
      });
      setAgents(response.data || []);
    } catch (error) {
      console.error('Error fetching agents:', error);
      setAgents([]);
    }
  };

  const handlePayTransaction = async (transactionID) => {
    try {
      const response = await axios.post(`${API_BASE_URL}/payTransaction`, {
        action: 'pay_transaction',
        transactionId: transactionID
      });
      refreshData();
    } catch (error) {
      console.error("Error paying transaction:", error);
    }
  };

  const refreshData = async () => {
    Promise.all([
      fetchAppointments(),
      fetchTransactions(),
      fetchAgents()
    ]).catch(error => {
      console.error('Error refreshing data:', error);
    });
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>Client Dashboard</h1>
      <div style={styles.profileSection}>
        <p>Client ID: {CLIENT_ID} </p>
        <p>Client Name: {FIRST_NAME} {LAST_NAME}</p>
        <p>Email: {EMAIL}</p>
        <p>Phone: {PHONE}</p>
        <p>Address: {STREET}, {STATE} {ZIPCODE}</p>
      </div>

      <section style={styles.section}>
        <h2>All Properties</h2>
        <ClientPropertyContainer
          CLIENT_ID={CLIENT_ID}
          updateData={refreshData}
        />
      </section>

      <section style={styles.section2}>
        <h2>View Your Appointments</h2>
        <div style={styles.scrollContainer}>
          {appointments.map((appointment, index) => (
            <div
              key={index}
              style={{
                ...styles.appointmentCard,
                marginRight: index !== appointments.length - 1 ? "20px" : "0",
              }}
            >
              <h2>Appointment {index + 1}</h2>
              <p>Client ID: {appointment.clientId}</p>
              <p>Agent ID: {appointment.agentId}</p>
              <p>Property ID: {appointment.propertyId}</p>
              <p>Date: {appointment.appointmentDate}</p>
              <p>Time: {appointment.appointmentTime}</p>
              <p>Purpose: {appointment.purpose}</p>
            </div>
          ))}
        </div>
      </section>

      <section style={styles.section2}>
        <h2>View Your Agents</h2>
        <div style={styles.scrollContainer}>
          {agents.map((agent, index) => (
            <div
              key={index}
              style={{
                ...styles.appointmentCard,
                marginRight: index !== agents.length - 1 ? "20px" : "0",
              }}
            >
              <h2>{`${agent.firstName} ${agent.lastName}`}</h2>
              <p>Email: {agent.email}</p>
              <p>Phone: {agent.phone}</p>
              <p>License Number: {agent.licenseNumber}</p>
              <p>Date Hired: {agent.dateHired}</p>
            </div>
          ))}
        </div>
      </section>

      <section style={styles.section2}>
        <h2>View Your Transactions</h2>
        <div style={styles.scrollContainer}>
          {transactions.map((transaction, index) => (
            <div
              key={index}
              style={{
                ...styles.appointmentCard,
                marginRight: index !== transactions.length - 1 ? "20px" : "0",
              }}
            >
              <h2>Transaction {index + 1}</h2>
              <p>Property ID: {transaction.propertyId}</p>
              <p>Agent ID: {transaction.agentId}</p>
              <p>Client ID: {transaction.clientId}</p>
              {transaction.dateSent ? (
                <p>Date Sent: {transaction.dateSent}</p>
              ) : (
                <p>Status: UNPAID</p>
              )}
              <p>Amount: {transaction.amount}</p>
              <p>Type: {transaction.transactionType}</p>
              {!transaction.dateSent && (
                <button
                  style={styles.button}
                  onClick={() => handlePayTransaction(transaction.transactionId)}
                >
                  Pay Transaction
                </button>
              )}
            </div>
          ))}
        </div>
      </section>
    </div>
  );
};

const styles = {
  container: {
    maxWidth: "800px",
    margin: "auto",
    padding: "20px",
    fontFamily: "Arial, sans-serif",
  },
  title: {
    textAlign: "center",
    fontSize: "24px",
    marginBottom: "20px",
  },
  section: {
    marginBottom: "30px",
  },
  inputContainer: {
    marginBottom: "15px",
  },
  input: {
    width: "100%",
    padding: "10px",
    fontSize: "16px",
    border: "1px solid #ccc",
    borderRadius: "5px",
  },
  input2: {
    width: "80%",
    padding: "10px",
    marginLeft: "20px",
    marginRight: "20px",
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
  label: {
    marginBottom: "8px",
  },
  textarea: {
    padding: "8px",
    marginBottom: "16px",
    border: "1px solid #ccc",
    borderRadius: "4px",
    fontSize: "14px",
    resize: "vertical",
  },
  profileSection: {
    fontSize: "14px",
    display: "flex",
    justifyContent: "space-between", // Distributes content evenly
    alignItems: "center", // Aligns items at the center vertically
    fontWeight: "200",
    marginBottom: "20px",
    borderTop: "2px solid #ccc",
    borderBottom: "2px solid #ccc",
    paddingBottom: "10px",
  },
  section2: {
    width: "100%",
    overflowX: "auto",
    whiteSpace: "nowrap",
  },
  scrollContainer: {
    display: "inline-block",
  },
  appointmentCard: {
    width: "200px",
    fontSize: "15px",
    border: "1px solid #ccc",
    padding: "10px",
    margin: "10px 0",
    display: "inline-block",
    verticalAlign: "top",
  },
};

export default ClientDashboard;
