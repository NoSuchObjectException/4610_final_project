import React, { useState, useEffect } from 'react';
import axios from 'axios';

const AgentPropertyContainer = ({ AGENT_ID, updateData }) => {
  const [properties, setProperties] = useState([]);
  const [propertyFormData, setPropertyFormData] = useState({
      propertyType: '',
      street: '',
      city: '',
      state: '',
      zipcode: '',
      listPrice: '',
      numBeds: '',
      numBaths: '',
      squareFootage: '',
      description: '',
      propertyStatus: 'AVAILABLE',
      image: '',
      agentId: AGENT_ID || ''
  });

  const [transactionFormData, setTransactionFormData] = useState({
      clientId: '',
      propertyId: '',
      amount: '',
      transactionType: '',
      dateSent: '',
      agentId: AGENT_ID || ''
  });

  const [propStatus, setPropStatus] = useState('');

  const API_BASE_URL = "https://acyx49drq5.execute-api.us-east-1.amazonaws.com/dev/api";

  const fetchProperties = async () => {
      try {
          if (!AGENT_ID) {
              console.log("No agent ID available for fetching properties");
              return;
          }
          
          console.log(`Fetching properties for agent: ${AGENT_ID}`);
          const response = await axios.post(`${API_BASE_URL}/getProperties`, {
              agentId: AGENT_ID
          });
          setProperties(response.data || []);
      } catch (error) {
          console.error("Error fetching properties:", error);
          setProperties([]);
      }
  };

  useEffect(() => {
      if (AGENT_ID) {
          console.log("Setting agent ID in form data:", AGENT_ID);
          setPropertyFormData(prev => ({ ...prev, agentId: AGENT_ID }));
          setTransactionFormData(prev => ({ ...prev, agentId: AGENT_ID }));
          fetchProperties();
      }
  }, [AGENT_ID]);

  const clearForms = () => {
      setPropStatus('');
      setPropertyFormData({
          propertyType: '',
          street: '',
          city: '',
          state: '',
          zipcode: '',
          listPrice: '',
          numBeds: '',
          numBaths: '',
          squareFootage: '',
          description: '',
          propertyStatus: 'AVAILABLE',
          image: '',
          agentId: AGENT_ID || ''
      });
      setTransactionFormData({
          clientId: '',
          propertyId: '',
          amount: '',
          transactionType: '',
          dateSent: '',
          agentId: AGENT_ID || ''
      });
  };

  const handleCreateTransaction = async (event) => {
      event.preventDefault();
      try {
          if (!transactionFormData.agentId || !transactionFormData.clientId || !transactionFormData.propertyId) {
              setPropStatus('Agent ID, Client ID, and Property ID are required');
              return;
          }

          const response = await axios.post(
              `${API_BASE_URL}/addTransaction`,
              {
                  agentId: transactionFormData.agentId,
                  clientId: transactionFormData.clientId,
                  propertyId: transactionFormData.propertyId,
                  amount: parseFloat(transactionFormData.amount),
                  transactionType: transactionFormData.transactionType,
                  dateSent: transactionFormData.dateSent || new Date().toISOString().split('T')[0]
              }
          );

          if (response.data) {
              setPropStatus("Successfully created transaction!");
              updateData();
              clearForms();
          } else {
              setPropStatus("Failed to create transaction.");
          }
      } catch (error) {
          setPropStatus("Error creating transaction: " + error.message);
          console.error("Transaction error:", error);
      }
  };

  const handleChangeTransaction = (e) => {
      const { name, value } = e.target;
      setTransactionFormData(prev => ({
          ...prev,
          [name]: value
      }));
  };

  const handleAddProperty = async (event) => {
      event.preventDefault();
      try {
          if (!propertyFormData.agentId) {
              setPropStatus('Agent ID is required');
              return;
          }

          const propertyPayload = {
              property: {
                  agentId: propertyFormData.agentId,
                  propertyType: propertyFormData.propertyType,
                  street: propertyFormData.street,
                  city: propertyFormData.city,
                  state: propertyFormData.state,
                  zipcode: propertyFormData.zipcode,
                  listPrice: parseFloat(propertyFormData.listPrice),
                  numBedrooms: parseInt(propertyFormData.numBeds),
                  numBathrooms: parseInt(propertyFormData.numBaths),
                  squareFootage: parseInt(propertyFormData.squareFootage),
                  description: propertyFormData.description,
                  status: propertyFormData.propertyStatus,
                  imageUrl: propertyFormData.image,
                  listingDate: new Date().toISOString().split('T')[0]
              }
          };

          console.log('Sending property data:', propertyPayload);
          const response = await axios.post(
              `${API_BASE_URL}/addProperty`,
              propertyPayload
          );

          if (response.data) {
              setPropStatus("Successfully uploaded property!");
              updateData();
              clearForms();
          } else {
              setPropStatus("Failed to upload property.");
          }
      } catch (error) {
          setPropStatus("Error uploading property: " + error.message);
          console.error("Property error:", error);
      }
  };

  const handleChangeProperty = (e) => {
      const { name, value } = e.target;
      setPropertyFormData(prev => ({
          ...prev,
          [name]: value
      }));
  };

  return (
      <div style={styles.container}>
          <section style={styles.section}>
              <h2>List a Property</h2>
              <form onSubmit={handleAddProperty} style={styles.inputContainer}>
                  <label style={styles.label}>
                      Property Type:
                      <input
                          style={styles.input}
                          type="text"
                          name="propertyType"
                          value={propertyFormData.propertyType}
                          onChange={handleChangeProperty}
                      />
                  </label>
                  <div style={styles.rowContainer}>
                      <label style={styles.label}>
                          Street:
                          <input
                              style={styles.input2}
                              type="text"
                              name="street"
                              value={propertyFormData.street}
                              onChange={handleChangeProperty}
                          />
                      </label>

                      <label style={styles.label}>
                          City:
                          <input
                              style={styles.input2}
                              type="text"
                              name="city"
                              value={propertyFormData.city}
                              onChange={handleChangeProperty}
                          />
                      </label>

                      <label style={styles.label}>
                          State:
                          <input
                              style={styles.input2}
                              type="text"
                              name="state"
                              value={propertyFormData.state}
                              onChange={handleChangeProperty}
                          />
                      </label>

                      <label style={styles.label}>
                          Zipcode:
                          <input
                              style={styles.input2}
                              type="text"
                              name="zipcode"
                              value={propertyFormData.zipcode}
                              onChange={handleChangeProperty}
                          />
                      </label>
                  </div>
                  
                  <label style={styles.label}>
                      List Price:
                      <input
                          style={styles.input}
                          type="number"
                          name="listPrice"
                          value={propertyFormData.listPrice}
                          onChange={handleChangeProperty}
                      />
                  </label>

                  <label style={styles.label}>
                      Number of Beds:
                      <input
                          style={styles.input}
                          type="number"
                          name="numBeds"
                          value={propertyFormData.numBeds}
                          onChange={handleChangeProperty}
                      />
                  </label>

                  <label style={styles.label}>
                      Number of Baths:
                      <input
                          style={styles.input}
                          type="number"
                          name="numBaths"
                          value={propertyFormData.numBaths}
                          onChange={handleChangeProperty}
                      />
                  </label>

                  <label style={styles.label}>
                      Square Footage:
                      <input
                          style={styles.input}
                          type="number"
                          name="squareFootage"
                          value={propertyFormData.squareFootage}
                          onChange={handleChangeProperty}
                      />
                  </label>

                  <label style={styles.label}>
                      Description:
                      <textarea
                          style={styles.input}
                          name="description"
                          value={propertyFormData.description}
                          onChange={handleChangeProperty}
                      />
                  </label>

                  <label style={styles.label}>
                      Status:
                      <select
                          style={styles.input}
                          name="propertyStatus"
                          value={propertyFormData.propertyStatus}
                          onChange={handleChangeProperty}
                      >
                          <option value="AVAILABLE">Available</option>
                          <option value="PENDING">Pending</option>
                          <option value="SOLD">Sold</option>
                      </select>
                  </label>

                  <label style={styles.label}>
                      Image URL:
                      <input
                          style={styles.input}
                          type="text"
                          name="image"
                          value={propertyFormData.image}
                          onChange={handleChangeProperty}
                      />
                  </label>

                  <button style={styles.button} type="submit">
                      Add Property
                  </button>
              </form>
              <p style={styles.status}>{propStatus}</p>
          </section>

          <section style={styles.section}>
              <h2>View Your Properties</h2>
              <div style={styles.scrollContainer}>
                  {properties.map((property, index) => (
                      <div
                          key={index}
                          style={{
                              ...styles.propertyCard,
                              marginRight: index !== properties.length - 1 ? "20px" : "0",
                          }}
                      >
                          <h3>{property.propertyType || 'Property'}</h3>
                          <p>{property.street}</p>
                          <p>{property.city}, {property.state} {property.zipcode}</p>
                          <p>Price: ${property.listPrice?.toLocaleString()}</p>
                          <p>Status: {property.status}</p>
                          <p>ID: {property.propertyId}</p>
                      </div>
                  ))}
              </div>
          </section>

          <section style={styles.section}>
              <h2>Create Transaction</h2>
              <form onSubmit={handleCreateTransaction} style={styles.inputContainer}>
                  <label style={styles.label}>
                      Client ID:
                      <input
                          style={styles.input}
                          type="text"
                          name="clientId"
                          value={transactionFormData.clientId}
                          onChange={handleChangeTransaction}
                      />
                  </label>
                  <label style={styles.label}>
                      Property ID:
                      <input
                          style={styles.input}
                          type="text"
                          name="propertyId"
                          value={transactionFormData.propertyId}
                          onChange={handleChangeTransaction}
                      />
                  </label>
                  <label style={styles.label}>
                      Amount:
                      <input
                          style={styles.input}
                          type="number"
                          name="amount"
                          value={transactionFormData.amount}
                          onChange={handleChangeTransaction}
                      />
                  </label>
                  <label style={styles.label}>
                      Transaction Type:
                      <select
                          style={styles.input}
                          name="transactionType"
                          value={transactionFormData.transactionType}
                          onChange={handleChangeTransaction}
                      >
                          <option value="">Select Type</option>
                          <option value="SALE">Sale</option>
                          <option value="PURCHASE">Purchase</option>
                          <option value="RENTAL">Rental</option>
                      </select>
                  </label>
                  <label style={styles.label}>
                      Date:
                      <input
                          style={styles.input}
                          type="date"
                          name="dateSent"
                          value={transactionFormData.dateSent}
                          onChange={handleChangeTransaction}
                      />
                  </label>
                  <button style={styles.button} type="submit">
                      Create Transaction
                  </button>
              </form>
              <p style={styles.status}>{propStatus}</p>
          </section>
      </div>
  );
};

const styles = {
    section: {
        marginBottom: "30px",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        textAlign: "center",
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
        width: "80%",
        padding: "10px",
        fontSize: "18px",
        backgroundColor: "#4CAF50",
        color: "white",
        border: "none",
        borderRadius: "5px",
        cursor: "pointer",
    },
    button2: {
        width: "150px",
        padding: "10px",
        fontSize: "15px",
        backgroundColor: "#4CAF50",
        color: "white",
        border: "none",
        borderRadius: "5px",
        cursor: "pointer",
    },
    label: {
        marginBottom: "8px",
    },
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
export default AgentPropertyContainer;
