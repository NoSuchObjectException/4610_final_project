# lambda_handler.py
import json
import boto3
import traceback
from typing import Dict, Any
from models import Property, Transaction, Office
from python_backend.Agent import agent_service
from service_extensions import PropertyService, TransactionService

def create_response(status_code: int, body: Any) -> Dict[str, Any]:
    return {
        'statusCode': status_code,
        'headers': {
            'Access-Control-Allow-Origin': '*', 
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
            'Content-Type': 'application/json'
        },
        'body': json.dumps(body) if not isinstance(body, str) else body
    }

class AgentLambdaHandler:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.property_service = PropertyService(self.dynamodb)
        self.transaction_service = TransactionService(self.dynamodb)

    def handle_property_request(self, event_body: dict) -> Dict[str, Any]:
        if 'action' not in event_body:
            return create_response(400, {'message': 'Action is required for property operations'})

        action = event_body['action']
        
        if action == 'add':
            try:
                property_data = event_body.get('property')
                if not property_data:
                    return create_response(400, {'message': 'Property data is required'})
                
                property_id = self.property_service.add_property(property_data)
                return create_response(200, {'propertyId': property_id})
            
            except Exception as e:
                return create_response(500, {
                    'message': 'Error adding property',
                    'error': str(e)
                })
                
        elif action == 'get':
            agent_id = event_body.get('agentId')
            if not agent_id:
                return create_response(400, {'message': 'Agent ID is required'})
                
            try:
                properties = self.property_service.get_properties_by_agent(agent_id)
                return create_response(200, properties)
            except Exception as e:
                return create_response(500, {
                    'message': 'Error retrieving properties',
                    'error': str(e)
                })
        
        return create_response(400, {'message': f'Unknown action: {action}'})

    def handle_transaction_request(self, event_body: dict) -> Dict[str, Any]:
        if 'action' not in event_body:
            return create_response(400, {'message': 'Action is required for transaction operations'})

        action = event_body['action']
        
        if action == 'add':
            try:
                transaction_data = event_body.get('transaction')
                if not transaction_data:
                    return create_response(400, {'message': 'Transaction data is required'})
                
                transaction_id = self.transaction_service.add_transaction(transaction_data)
                return create_response(200, {'transactionId': transaction_id})
                
            except Exception as e:
                return create_response(500, {
                    'message': 'Error adding transaction',
                    'error': str(e)
                })
                
        elif action == 'get':
            agent_id = event_body.get('agentId')
            if not agent_id:
                return create_response(400, {'message': 'Agent ID is required'})
                
            try:
                transactions = self.transaction_service.get_transactions_by_agent(agent_id)
                return create_response(200, transactions)
            except Exception as e:
                return create_response(500, {
                    'message': 'Error retrieving transactions',
                    'error': str(e)
                })
        
        return create_response(400, {'message': f'Unknown action: {action}'})

def handler(event, context):
    # Handle OPTIONS request for CORS
    if event.get('httpMethod') == 'OPTIONS':
        return create_response(200, {'message': 'OK'})
        
    try:
        # Your existing handler code...
        body = json.loads(event['body'])
        agent_id = body.get('agentId')
        
        if not agent_id:
            return create_response(400, {'message': 'agentId is required'})
            
        # Get agent data
        agent = agent_service.get_agent(agent_id)
        if not agent:
            return create_response(404, {'message': 'Agent not found'})
            
        return create_response(200, agent)
        
    except Exception as e:
        return create_response(500, {
            'message': 'Internal server error',
            'error': str(e)
        })