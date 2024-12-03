# client_service.py
from typing import Optional, List, Dict, Any
import uuid
from datetime import datetime
from boto3.dynamodb.conditions import Key
from client_models import Client, ClientAgent, Appointment

class ClientService:
    def __init__(self, dynamodb_resource):
        self.dynamodb = dynamodb_resource
        self.table_prefix = 'dev-'

    def _get_table(self, table_name: str):
        return self.dynamodb.Table(f"{self.table_prefix}{table_name}")

    def get_client(self, client_id: str) -> Optional[Dict[str, Any]]:
        try:
            table = self._get_table('Client')
            response = table.get_item(Key={'clientId': client_id})
            return response.get('Item')
        except Exception as e:
            print(f"Error getting client: {str(e)}")
            raise

    def get_properties(self) -> List[Dict[str, Any]]:
        try:
            print("[DEBUG] Attempting to get properties")
            table = self._get_table('Property')
            print(f"[DEBUG] Accessing table: {self.table_prefix}Property")
            response = table.scan()
            print(f"[DEBUG] Scan response: {response}")
            return response.get('Items', [])
        except Exception as e:
            print(f"[DEBUG] Error getting properties: {str(e)}")
            print(f"[DEBUG] Error type: {type(e)}")
            raise

    def get_property_agent(self, agent_id: str) -> Optional[Dict[str, Any]]:
        try:
            table = self._get_table('Agent')
            response = table.get_item(Key={'agentId': agent_id})
            return response.get('Item')
        except Exception as e:
            print(f"Error getting agent: {str(e)}")
            raise

    def add_appointment(self, appointment_data: Dict[str, Any]) -> str:
        try:
            # Create appointment
            appointment_id = str(uuid.uuid4())
            appointment_data['appointmentId'] = appointment_id
            
            appointments_table = self._get_table('Appointment')
            appointments_table.put_item(Item=appointment_data)
            
            # Create client-agent relationship
            client_agent_data = {
                'id': ClientAgent.generate_id(
                    appointment_data['clientId'],
                    appointment_data['agentId']
                ),
                'clientId': appointment_data['clientId'],
                'agentId': appointment_data['agentId'],
                'relationshipDate': datetime.now().isoformat(),
                'status': 'ACTIVE'
            }
            
            client_agent_table = self._get_table('ClientAgent')
            client_agent_table.put_item(Item=client_agent_data)
            
            return appointment_id
        except Exception as e:
            print(f"Error adding appointment: {str(e)}")
            raise

    def query_with_index(self, table_name: str, index_name: str, 
                    key_name: str, key_value: str) -> List[Dict[str, Any]]:
        print(f"[QUERY DEBUG] Starting query with parameters:")
        print(f"[QUERY DEBUG] Table: {table_name}")
        print(f"[QUERY DEBUG] Index: {index_name}")
        print(f"[QUERY DEBUG] Key: {key_name}={key_value}")
        
        table = self._get_table(table_name)
        try:
            # First, verify the table exists
            try:
                table.table_status
                print(f"[QUERY DEBUG] Table {table_name} exists and is accessible")
            except Exception as e:
                print(f"[QUERY DEBUG] Error accessing table: {str(e)}")
                raise

            # Attempt the query
            print(f"[QUERY DEBUG] Executing query on table")
            response = table.query(
                IndexName=index_name,
                KeyConditionExpression=f"{key_name} = :value",
                ExpressionAttributeValues={
                    ':value': key_value
                }
            )
            
            items = response.get('Items', [])
            print(f"[QUERY DEBUG] Query successful. Found {len(items)} items")
            if len(items) > 0:
                print(f"[QUERY DEBUG] Sample item keys: {list(items[0].keys())}")
            return items
        
        except Exception as e:
            print(f"[QUERY DEBUG] Error executing query: {str(e)}")
            print(f"[QUERY DEBUG] Error type: {type(e).__name__}")
            raise

    def get_appointments(self, client_id: str) -> List[Dict[str, Any]]:
        print(f"[APPOINTMENT DEBUG] Getting appointments for client: {client_id}")
        try:
            # First, verify the client exists
            client_table = self._get_table('Client')
            client = client_table.get_item(Key={'clientId': client_id}).get('Item')
            if not client:
                print(f"[APPOINTMENT DEBUG] Client {client_id} not found")
                return []
            
            print(f"[APPOINTMENT DEBUG] Client {client_id} exists, fetching appointments")
            result = self.query_with_index('Appointment', 'client-index', 'clientId', client_id)
            print(f"[APPOINTMENT DEBUG] Retrieved {len(result)} appointments")
            
            # Log the structure of each appointment for debugging
            for idx, appt in enumerate(result):
                print(f"[APPOINTMENT DEBUG] Appointment {idx + 1} structure:")
                print(f"[APPOINTMENT DEBUG] Keys: {list(appt.keys())}")
            
            return result
        except Exception as e:
            print(f"[APPOINTMENT DEBUG] Error: {str(e)}")
            print(f"[APPOINTMENT DEBUG] Error type: {type(e).__name__}")
            raise

    def get_agents(self, client_id: str) -> List[Dict[str, Any]]:
        print(f"[SERVICE] Getting agents for client: {client_id}")
        try:
            client_agents = self.query_with_index('ClientAgent', 'client-index', 'clientId', client_id)
            print(f"[SERVICE] Found {len(client_agents)} client-agent relationships")
            
            agent_table = self._get_table('Agent')
            agents = []
            
            for ca in client_agents:
                print(f"[SERVICE] Fetching agent {ca['agentId']}")
                response = agent_table.get_item(Key={'agentId': ca['agentId']})
                if 'Item' in response:
                    agents.append(response['Item'])
            
            print(f"[SERVICE] Retrieved {len(agents)} agents")
            return agents
        except Exception as e:
            print(f"[ERROR] Failed to get agents: {str(e)}")
            raise

    def get_transactions(self, client_id: str) -> List[Dict[str, Any]]:
        print(f"[SERVICE] Getting transactions for client: {client_id}")
        try:
            result = self.query_with_index('Transaction', 'client-index', 'clientId', client_id)
            print(f"[SERVICE] Found {len(result)} transactions")
            return result
        except Exception as e:
            print(f"[ERROR] Failed to get transactions: {str(e)}")
            raise

    def pay_transaction(self, transaction_id: str) -> None:
        try:
            table = self._get_table('Transaction')
            table.update_item(
                Key={'transactionId': transaction_id},
                UpdateExpression='SET dateSent = :date',
                ExpressionAttributeValues={
                    ':date': datetime.now().isoformat()
                }
            )
        except Exception as e:
            print(f"Error paying transaction: {str(e)}")
            raise