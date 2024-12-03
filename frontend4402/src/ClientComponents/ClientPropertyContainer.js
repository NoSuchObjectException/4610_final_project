import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faChevronLeft, faChevronRight } from '@fortawesome/free-solid-svg-icons';
import './clientProp.css';

const PropertyContainer = ({ CLIENT_ID, updateData }) => {
  const [properties, setProperties] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [agent, setAgent] = useState({});
  const [apptStatus, setApptStatus] = useState('');

  const API_BASE_URL = "https://5pq8iah053.execute-api.us-east-1.amazonaws.com/dev/api";

  const [appointmentForm, setAppointmentForm] = useState({
    appt_date: "",
    appt_time: "",
    purpose: "",
  });

  const handleAddAppointment = async () => {
    try {
      const currentProperty = properties[currentIndex];
      console.log('Current property data:', currentProperty);
      
      const propertyId = currentProperty?.propertyId || currentProperty?.PROPERTY_ID;
      const agentId = currentProperty?.agentId || currentProperty?.AGENT_ID;
      
      if (!agentId || !CLIENT_ID || !propertyId) {
        console.error('Missing required fields:', { agentId, clientId: CLIENT_ID, propertyId });
        setApptStatus("Missing required information. Please contact support.");
        return;
      }
  
      const appointmentDateTime = `${appointmentForm.appt_date}T${appointmentForm.appt_time}:00`;
      
      const appointmentData = {
        action: 'add_appointment',
        clientId: CLIENT_ID,
        appointment: {
          agentId: agentId,
          clientId: CLIENT_ID,
          propertyId: propertyId,
          appointmentDate: appointmentDateTime,
          purpose: appointmentForm.purpose,
          status: 'SCHEDULED'
        }
      };
  
      console.log('Sending appointment data:', appointmentData);
  
      // Changed from /api/addAppointment to /api to match other working endpoints
      const response = await axios.post(`${API_BASE_URL}/addAppointment`, appointmentData);
      
      console.log('Appointment response:', response.data);
  
      if (response.data) {
        setApptStatus("Successfully scheduled appointment!");
        updateData();
        setAppointmentForm({
          appt_date: "",
          appt_time: "",
          purpose: "",
        });
      }
    } catch (error) {
      const errorMessage = error.response?.data?.message || error.message;
      console.error("Error adding appointment:", error.response?.data || error);
      setApptStatus("Error adding appointment: " + errorMessage);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setAppointmentForm(prev => ({
      ...prev,
      [name]: value
    }));
  };

  useEffect(() => {
    const fetchProperties = async () => {
      try {
        const response = await axios.post(`${API_BASE_URL}/getProperties`, {
          action: 'get_properties'
        });
        console.log('Raw property data:', response.data); // Debug log
        
        // Transform the data to ensure consistent field names
        const transformedProperties = (response.data || []).map(property => ({
          ...property,
          AGENT_ID: property.agentId || property.AGENT_ID,
          PROPERTY_ID: property.propertyId || property.PROPERTY_ID,
          // Add other field transformations as needed
        }));
        
        console.log('Transformed properties:', transformedProperties); // Debug log
        setProperties(transformedProperties);
      } catch (error) {
        console.error('Error fetching properties:', error);
        setProperties([]);
      }
    };

    fetchProperties();
  }, []);


  const handleGetPropertyAgent = async (agentId) => {
    console.log('Property data:', properties[currentIndex]); // Debug log
    
    if (!agentId) {
      console.error('No agentId available');
      setApptStatus('Error: Agent ID not found');
      return;
    }
    
    try {
      const response = await axios.post(`${API_BASE_URL}/getAgent`, {
        action: 'get_property_agent',
        agentId: agentId,
        clientId: CLIENT_ID
      });
      console.log('Agent response:', response.data); // Debug log
      setAgent(response.data || {});
    } catch (error) {
      console.error('Error fetching agent:', error.response?.data || error);
      setAgent({});
    }
  };
  

  const handleKeyDown = useCallback((event) => {
    if (event.keyCode === 37) {
      // Left arrow key
      setCurrentIndex(prevIndex => (prevIndex === 0 ? properties.length - 1 : prevIndex - 1));
    } else if (event.keyCode === 39) {
      // Right arrow key
      setCurrentIndex(prevIndex => (prevIndex === properties.length - 1 ? 0 : prevIndex + 1));
    }
  }, [properties.length]);

  useEffect(() => {
    window.addEventListener('keydown', handleKeyDown);
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [handleKeyDown]);

  const navigateProperty = (direction) => {
    if (direction === 'prev') {
      setCurrentIndex(prevIndex => (prevIndex === 0 ? properties.length - 1 : prevIndex - 1));
    } else if (direction === 'next') {
      setCurrentIndex(prevIndex => (prevIndex === properties.length - 1 ? 0 : prevIndex + 1));
    }
    setAgent({});
  };

  if (!properties.length) {
    return <div>Loading properties...</div>;
  }

  return (
    <div className="property-container">
      <div className="custom-slide">
        <div className="arrow left-arrow" onClick={() => navigateProperty('prev')}>
          <FontAwesomeIcon icon={faChevronLeft} />
        </div>
        <div className="property-content">
          <h2>{properties[currentIndex].PROPERTY_TYPE}</h2>
          <img 
            className='image' 
            src={properties[currentIndex].IMAGE_URL} 
            alt="Property" 
            onError={(e) => {
              e.target.src = 'https://via.placeholder.com/400x300?text=No+Image+Available';
            }}
          />
          <p>{properties[currentIndex].STREET}, {properties[currentIndex].CITY}, {properties[currentIndex].STATE} - {properties[currentIndex].ZIPCODE}</p>
          <p>Price: ${properties[currentIndex].LIST_PRICE?.toLocaleString()} </p>
          <p>Bedrooms: {properties[currentIndex].NUM_BEDROOMS} Bathrooms: {properties[currentIndex].NUM_BATHROOMS}</p>
          <p>{properties[currentIndex].DESCRIPTION}</p>

          <button 
            style={styles.button2} 
            onClick={() => handleGetPropertyAgent(properties[currentIndex].AGENT_ID)}
          >
            Get Contact Info
          </button>
          
          {Object.keys(agent).length > 0 ? (
            <div>
              <p>Agent Information: {agent.firstName} {agent.lastName}</p>
              <p>Email: {agent.email}</p>
              <p>Phone: {agent.phone}</p>
            </div>
          ) : (
            <div>
              <p>Click above to see Agent Information!</p>
            </div>
          )}
        </div>
        <div className="arrow right-arrow" onClick={() => navigateProperty('next')}>
          <FontAwesomeIcon icon={faChevronRight} />
        </div>
      </div>

      <section style={styles.section}>
        <h3>Schedule an Appointment for this {properties[currentIndex].PROPERTY_TYPE} Now!</h3>
        <div style={styles.appointmentForm}>
          <div style={styles.formRow}>
            <label style={styles.label}>
              Appointment Date:
              <input
                style={styles.input2}
                type="date"
                name="appt_date"
                value={appointmentForm.appt_date}
                onChange={handleChange}
              />
            </label>

            <label style={styles.label}>
              Appointment Time:
              <input
                style={styles.input2}
                type="time"
                min="09:00"
                max="17:00"
                name="appt_time"
                value={appointmentForm.appt_time}
                onChange={handleChange}
              />
            </label>
          </div>
          
          <label style={styles.label}>
            Appointment Purpose:
            <input
              style={styles.input2}
              type="text"
              name="purpose"
              maxLength={50}
              value={appointmentForm.purpose}
              onChange={handleChange}
              placeholder="Brief description of appointment purpose"
            />
          </label>

          <button 
            style={styles.button} 
            onClick={handleAddAppointment}
            disabled={!appointmentForm.appt_date || !appointmentForm.appt_time || !appointmentForm.purpose}
          >
            Schedule Appointment
          </button>
          {apptStatus && <p style={styles.status}>{apptStatus}</p>}
        </div>
      </section>
    </div>
  );
};

const styles = {
  section: {
    marginBottom: '30px',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    textAlign: 'center',
  },
  appointmentForm: {
    width: '100%',
    maxWidth: '600px',
    padding: '20px',
  },
  formRow: {
    display: 'flex',
    justifyContent: 'space-between',
    marginBottom: '20px',
    gap: '20px',
  },
  input: {
    width: "100%",
    padding: "10px",
    fontSize: "16px",
    border: "1px solid #ccc",
    borderRadius: "5px",
  },
  input2: {
    width: "100%",
    padding: "10px",
    fontSize: "16px",
    border: "1px solid #ccc",
    borderRadius: "5px",
    marginTop: '5px',
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
    marginTop: '20px',
    ':disabled': {
      backgroundColor: '#cccccc',
      cursor: 'not-allowed',
    }
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
    marginBottom: '10px',
  },
  label: {
    marginBottom: '8px',
    display: 'flex',
    flexDirection: 'column',
    flex: 1,
    textAlign: 'left',
  },
  status: {
    marginTop: '10px',
    color: '#4CAF50',
    fontWeight: 'bold',
  }
};

export default PropertyContainer;