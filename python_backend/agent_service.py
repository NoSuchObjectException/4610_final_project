# agent_service.py
import boto3
from typing import Optional, Dict, Any, List
import uuid
from datetime import datetime
from botocore.exceptions import ClientError
from decimal import Decimal

class AgentService:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.table_prefix = 'dev-'

    def _get_table(self, table_name: str):
        """Helper method to get table with proper prefix"""
        return self.dynamodb.Table(f"{self.table_prefix}{table_name}")

    def get_agent(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get agent by ID"""
        try:
            if not agent_id or not agent_id.strip():
                raise ValueError("Agent ID cannot be null or empty")

            table = self._get_table('Agent')
            response = table.get_item(Key={'agentId': agent_id})
            return response.get('Item')

        except Exception as e:
            print(f"Error getting agent: {str(e)}")
            raise

    def get_agent_properties(self, agent_id: str) -> List[Dict[str, Any]]:
        """Get properties by agent ID"""
        try:
            table = self._get_table('Property')
            response = table.query(
                IndexName='agent-index',
                KeyConditionExpression='agentId = :agentId',
                ExpressionAttributeValues={':agentId': agent_id}
            )
            return response.get('Items', [])
        except Exception as e:
            print(f"Error getting properties: {str(e)}")
            raise

    def get_appointments(self, agent_id: str) -> List[Dict[str, Any]]:
        """Get appointments by agent ID"""
        try:
            table = self._get_table('Appointment')
            response = table.query(
                IndexName='agent-date-index',
                KeyConditionExpression='agentId = :agentId',
                ExpressionAttributeValues={':agentId': agent_id}
            )
            # Convert response to match frontend expectations
            appointments = []
            for item in response.get('Items', []):
                appointments.append({
                    'APPT_TIME': item.get('appointmentTime'),
                    'APPT_DATE': item.get('appointmentDate'),
                    'PURPOSE': item.get('purpose'),
                    'CLIENT_ID': item.get('clientId'),
                    'PROPERTY_ID': item.get('propertyId')
                })
            return appointments
        except Exception as e:
            print(f"Error getting appointments: {str(e)}")
            raise

    def get_clients(self, agent_id: str) -> List[Dict[str, Any]]:
        """Get clients by agent ID"""
        try:
            # Get client-agent relationships
            ca_table = self._get_table('ClientAgent')
            client_agents = ca_table.query(
                IndexName='agent-index',
                KeyConditionExpression='agentId = :agentId',
                ExpressionAttributeValues={':agentId': agent_id}
            ).get('Items', [])

            # Get client details
            client_table = self._get_table('Client')
            clients = []
            
            for ca in client_agents:
                response = client_table.get_item(
                    Key={'clientId': ca['clientId']}
                )
                if 'Item' in response:
                    client = response['Item']
                    # Convert to frontend expected format
                    clients.append({
                        'CLIENT_FIRST_NAME': client.get('firstName'),
                        'CLIENT_LAST_NAME': client.get('lastName'),
                        'CLIENT_EMAIL': client.get('email'),
                        'CLIENT_PHONE': client.get('phone'),
                        'CLIENT_STREET': client.get('street'),
                        'CLIENT_CITY': client.get('city'),
                        'CLIENT_ZIPCODE': client.get('zipcode')
                    })
            return clients
        except Exception as e:
            print(f"Error getting clients: {str(e)}")
            raise

    def get_transactions(self, agent_id: str) -> List[Dict[str, Any]]:
        """Get transactions by agent ID"""
        try:
            table = self._get_table('Transaction')
            try:
                response = table.query(
                    IndexName='agent-index',
                    KeyConditionExpression='agentId = :agentId',
                    ExpressionAttributeValues={':agentId': agent_id}
                )
                # Convert to frontend expected format
                transactions = []
                for item in response.get('Items', []):
                    transactions.append({
                        'TRANSACTION_ID': item.get('transactionId'),
                        'CLIENT_ID': item.get('clientId'),
                        'DATE_SENT': item.get('dateSent'),
                        'AMOUNT': item.get('amount'),
                        'TYPE': item.get('transactionType')
                    })
                return transactions
            except self.dynamodb.meta.client.exceptions.ResourceNotFoundException:
                print(f"Transaction table or index not found for agent {agent_id}")
                return []
        except Exception as e:
            print(f"Error getting transactions: {str(e)}")
            # Return empty list instead of raising to prevent UI disruption
            return []

    def get_office(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get office details for an agent"""
        try:
            # First get the agent to get the officeId
            agent = self.get_agent(agent_id)
            if not agent or 'officeId' not in agent:
                print(f"No office ID found for agent {agent_id}")
                return [{
                    'STREET': 'No office assigned',
                    'CITY': '',
                    'ZIPCODE': '',
                    'PHONE': ''
                }]

            try:
                # Then get the office details
                table = self._get_table('Office')
                response = table.get_item(Key={'officeId': agent['officeId']})
                office = response.get('Item')
                
                if office:
                    # Convert to frontend expected format
                    return [{
                        'STREET': office.get('street'),
                        'CITY': office.get('city'),
                        'ZIPCODE': office.get('zipcode'),
                        'PHONE': office.get('phone')
                    }]
                
                # Return placeholder if no office data found
                return [{
                    'STREET': 'Office data not found',
                    'CITY': '',
                    'ZIPCODE': '',
                    'PHONE': ''
                }]

            except Exception as e:
                print(f"Error accessing Office table: {str(e)}")
                # Return placeholder if table doesn't exist
                return [{
                    'STREET': 'Office system unavailable',
                    'CITY': '',
                    'ZIPCODE': '',
                    'PHONE': ''
                }]

        except Exception as e:
            print(f"Error getting office: {str(e)}")
            raise

    def add_property(self, property_data: Dict[str, Any]) -> str:
        """Add a new property with validation"""
        try:
            # Ensure numeric values are Decimal/int for DynamoDB
            if not isinstance(property_data['listPrice'], Decimal):
                property_data['listPrice'] = Decimal(str(property_data['listPrice']))
            property_data['numBedrooms'] = int(property_data['numBedrooms'])
            property_data['numBathrooms'] = int(property_data['numBathrooms'])
            property_data['squareFootage'] = int(property_data['squareFootage'])

            # Validate numeric values
            if property_data['listPrice'] <= 0:
                raise ValueError("List price must be greater than 0")
            if property_data['numBedrooms'] < 0:
                raise ValueError("Number of bedrooms cannot be negative")
            if property_data['numBathrooms'] < 0:
                raise ValueError("Number of bathrooms cannot be negative")
            if property_data['squareFootage'] <= 0:
                raise ValueError("Square footage must be greater than 0")

            # Validate status
            valid_statuses = ['AVAILABLE', 'PENDING', 'SOLD']
            if property_data['status'] not in valid_statuses:
                raise ValueError(f"Invalid status. Must be one of: {', '.join(valid_statuses)}")

            # Generate UUID if not provided
            if 'propertyId' not in property_data:
                property_data['propertyId'] = str(uuid.uuid4())

            # Add to database
            table = self._get_table('Property')
            table.put_item(Item=property_data)
            
            return property_data['propertyId']

        except Exception as e:
            print(f"Error adding property: {str(e)}")
            raise ValueError(f"Failed to add property: {str(e)}")

    def add_transaction(self, transaction_data: Dict[str, Any]) -> str:
        """Add a new transaction"""
        try:
            # Ensure numeric values are Decimal for DynamoDB
            if not isinstance(transaction_data['amount'], Decimal):
                transaction_data['amount'] = Decimal(str(transaction_data['amount']))

            # Validate amount
            if transaction_data['amount'] <= 0:
                raise ValueError("Transaction amount must be greater than 0")

            # Validate transaction type
            valid_types = ['SALE', 'PURCHASE', 'RENTAL']
            if transaction_data['transactionType'] not in valid_types:
                raise ValueError(f"Invalid transaction type. Must be one of: {', '.join(valid_types)}")

            # Generate transaction ID
            transaction_data['transactionId'] = str(uuid.uuid4())
            
            # Add timestamp if not provided
            if 'timestamp' not in transaction_data:
                transaction_data['timestamp'] = datetime.now().isoformat()

            # Add to database
            table = self._get_table('Transaction')
            table.put_item(Item=transaction_data)
            
            return transaction_data['transactionId']

        except Exception as e:
            print(f"Error adding transaction: {str(e)}")
            raise ValueError(f"Failed to add transaction: {str(e)}")