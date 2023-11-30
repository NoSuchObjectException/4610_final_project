package com.example.backend4402.Agent;

import org.apache.tomcat.util.json.JSONParser;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.time.LocalDate;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/agent")
public class AgentController {

    private final AgentService agentService;

    @Autowired
    public AgentController(AgentService myService) {
        this.agentService = myService;
    }

    @PostMapping("/getAgent")
    public Map<String, Object> getAgent(@RequestBody Map<String, String> arguments){
        Long agentID = Long.parseLong(arguments.get("agentID"));
        List<Map<String, Object>> agent = agentService.getAgent(agentID);
        Map<String, Object> agentobj = agent.get(0);
        agentobj.put("agentID", agentID);
        return agentobj;
    }

    @PostMapping("/addProperty")
    public int addProperty(@RequestBody Map<String, String> arguments) {
        String agentID = arguments.get("agentID");
        String propertyType = arguments.get("propertyType");
        String street = arguments.get("street");
        String city = arguments.get("city");
        String state = arguments.get("state");
        String zipcode = arguments.get("zipcode");
        String listPrice = arguments.get("listPrice");
        String numBeds = arguments.get("numBeds");
        String numBaths = arguments.get("numBaths");
        String squareFootage = arguments.get("squareFootage");
        String description = arguments.get("description");
        String date = LocalDate.now().toString();
        String status = arguments.get("propertyStatus");
        String image = arguments.get("image");

        String sql2 = "INSERT INTO PROPERTY (AGENT_ID, PROPERTY_TYPE, STREET, CITY, STATE, ZIPCODE, LIST_PRICE, NUM_BEDROOMS, NUM_BATHROOMS, SQUARE_FOOTAGE, DESCRIPTION, LISTING_DATE, STATUS, IMAGE_URL) VALUES ("
                + agentID + ",'" + propertyType + "','" + street + "','" + city + "','"
                + state
                + "'," + zipcode + "," + listPrice + "," + numBeds + ","
                + numBaths + "," + squareFootage + ",'" + description + "','" + date + "','" + status + "','" + image + "');";

        try {
            int propertyID = agentService.addProperty(sql2);
            return propertyID;
        } catch (Exception e) {
            e.printStackTrace();
            return -1;
        }
    }

    @PostMapping("/getProperties")
    public List<Map<String, Object>> getAgentProperties(@RequestBody Map<String, String> arguments) {
        String agentID = arguments.get("agentID");
        String sql = "SELECT * FROM PROPERTY WHERE AGENT_ID = " + agentID;
        return agentService.getProperties(sql);
    }

    @PostMapping("/getAppointments")
    public List<Map<String, Object>> getAppointments(@RequestBody Map<String, String> arguments) {
        String agentID = arguments.get("agentID");
        String sql = "SELECT * FROM APPOINTMENT WHERE AGENT_ID = " + agentID;
        return agentService.getAppointments(sql);
    }

    @PostMapping("/getOffice")
    public List<Map<String, Object>> getOffice(@RequestBody Map<String, String> arguments) {
        String agentID = arguments.get("agentID");
        // implement
        return null;
    }

    @PostMapping("/getClients")
    public List<Map<String, Object>> getClients(@RequestBody Map<String, String> arguments) {
        String agentID = arguments.get("agentID");
        String sql = "SELECT * FROM CLIENT";
        return agentService.getClients(sql);
    }

    @PostMapping("/addTransaction")
    public List<Map<String, Object>> addTransaction(@RequestBody Map<String, String> arguments) {
        String agentID = arguments.get("agentID");
        String clientID = arguments.get("clientID");
        String amount = arguments.get("Amount");
        String transactionType = arguments.get("transactionType");

        String sql = "";
        return null;
    }

    @PostMapping("/getTransactions")
    public List<Map<String, Object>> getTransactions(@RequestBody Map<String, String> arguments) {
        String agentID = arguments.get("agentID");
        String sql = "SELECT * FROM TRANSACTION WHERE AGENT_ID = " + agentID;
        return agentService.getTransactions(sql);
    }
}
