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
            table = self._get_table('Property')
            response = table.scan()
            return response.get('Items', [])
        except Exception as e:
            print(f"Error getting properties: {str(e)}")
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
        print(f"[QUERY] Querying {table_name} with index {index_name} for {key_name}={key_value}")
        table = self._get_table(table_name)
        try:
            response = table.query(
                IndexName=index_name,
                KeyConditionExpression=Key(key_name).eq(key_value)
            )
            items = response.get('Items', [])
            print(f"[QUERY] Found {len(items)} items in {table_name}")
            return items
        except Exception as e:
            print(f"[ERROR] Failed to query {table_name}: {str(e)}")
            raise

    def get_appointments(self, client_id: str) -> List[Dict[str, Any]]:
        print(f"[SERVICE] Getting appointments for client: {client_id}")
        try:
            result = self.query_with_index('Appointment', 'client-index', 'clientId', client_id)
            print(f"[SERVICE] Found {len(result)} appointments")
            return result
        except Exception as e:
            print(f"[ERROR] Failed to get appointments: {str(e)}")
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