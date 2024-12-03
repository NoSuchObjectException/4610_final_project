# client_lambda_handler.py
import json
import boto3
import traceback
import uuid
from typing import Dict, Any
from decimal import Decimal
from client_service import ClientService

class DecimalEncoder(json.JSONEncoder):
    """Custom JSON encoder to handle Decimal types"""
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return super(DecimalEncoder, self).default(obj)

def create_response(status_code: int, body: Any) -> Dict[str, Any]:
    print(f"Creating response with status code: {status_code} and body: {body}")
    return {
        'statusCode': status_code,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
            'Content-Type': 'application/json'
        },
        'body': json.dumps(body, cls=DecimalEncoder) if not isinstance(body, str) else body
    }

class ClientLambdaHandler:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.client_service = ClientService(self.dynamodb)

    def handle_client_request(self, event_body: dict) -> Dict[str, Any]:
        print(f"[REQUEST START] Processing client request with body: {json.dumps(event_body)}")
        request_id = str(uuid.uuid4())
        
        action = event_body.get('action')
        if not action:
            print(f"[{request_id}] No action provided in request")
            return create_response(400, {'message': 'Action is required'})

        # Special case for get_properties which doesn't require clientId
        if action == 'get_properties':
            print(f"[{request_id}] Fetching all properties")
            try:
                properties = self.client_service.get_properties()
                print(f"[{request_id}] Retrieved {len(properties)} properties")
                return create_response(200, properties)
            except Exception as e:
                error_details = {
                    'requestId': request_id,
                    'message': 'Error retrieving properties',
                    'error': str(e),
                    'type': e.__class__.__name__,
                    'action': action
                }
                print(f"[{request_id}] Error details: {json.dumps(error_details)}")
                return create_response(500, error_details)

        # For all other actions, require clientId
        client_id = event_body.get('clientId')
        if not client_id and action != 'get_properties':
            print(f"[{request_id}] No clientId provided in request")
            return create_response(400, {'message': 'Client ID is required'})

        try:
            print(f"[{request_id}] Executing {action} for client: {client_id}")
            
            if action == 'get_property_agent':
                agent_id = event_body.get('agentId')
                if not agent_id:
                    return create_response(400, {'message': 'agentId is required'})
                agent = self.client_service.get_property_agent(agent_id)
                if not agent:
                    return create_response(404, {'message': 'Agent not found'})
                return create_response(200, agent)

            if action == 'get_appointments':
                print(f"[{request_id}] Fetching appointments for client {client_id}")
                appointments = self.client_service.get_appointments(client_id)
                print(f"[{request_id}] Retrieved {len(appointments)} appointments")
                return create_response(200, appointments)

            elif action == 'get_agents':
                print(f"[{request_id}] Fetching agents for client {client_id}")
                agents = self.client_service.get_agents(client_id)
                print(f"[{request_id}] Retrieved {len(agents)} agents")
                return create_response(200, agents)

            elif action == 'get_transactions':
                print(f"[{request_id}] Fetching transactions for client {client_id}")
                transactions = self.client_service.get_transactions(client_id)
                print(f"[{request_id}] Retrieved {len(transactions)} transactions")
                return create_response(200, transactions)

            elif action == 'get_client':
                client = self.client_service.get_client(client_id)
                if not client:
                    return create_response(404, {'message': 'Client not found'})
                return create_response(200, client)

            elif action == 'add_appointment':
                appointment_data = event_body.get('appointment')
                if not appointment_data:
                    return create_response(400, {'message': 'Appointment data is required'})
                
                appointment_id = self.client_service.add_appointment(appointment_data)
                return create_response(200, {'appointmentId': appointment_id})

            elif action == 'pay_transaction':
                transaction_id = event_body.get('transactionId')
                if not transaction_id:
                    return create_response(400, {'message': 'Transaction ID is required'})
                
                self.client_service.pay_transaction(transaction_id)
                return create_response(200, {'message': 'Transaction paid successfully'})

            else:
                return create_response(400, {'message': f'Unknown action: {action}'})

        except Exception as e:
            error_details = {
                'requestId': request_id,
                'message': 'Error processing request',
                'error': str(e),
                'type': e.__class__.__name__,
                'action': action,
                'clientId': client_id
            }
            print(f"[{request_id}] Error details: {json.dumps(error_details)}")
            print(f"[{request_id}] Stack trace: {traceback.format_exc()}")
            return create_response(500, error_details)

def handler(event, context):
    print(f"Received event: {json.dumps(event)}")
    
    # Handle OPTIONS requests for CORS preflight
    if event.get('httpMethod') == 'OPTIONS':
        print("Handling OPTIONS preflight request")
        return create_response(200, 'OK')

    try:
        if not event.get('body'):
            print("No request body provided")
            return create_response(400, {'message': 'Request body is required'})
            
        body = json.loads(event['body'])
        print(f"Parsed request body: {json.dumps(body)}")
        
        client_handler = ClientLambdaHandler()
        response = client_handler.handle_client_request(body)
        print(f"Handler response: {json.dumps(response)}")
        return response
        
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {str(e)}")
        return create_response(400, {'message': 'Invalid JSON in request body'})
    except Exception as e:
        error_details = {
            'message': 'Internal server error',
            'error': str(e),
            'type': e.__class__.__name__,
            'stackTrace': traceback.format_exc()
        }
        print(f"Error processing request: {json.dumps(error_details)}")
        return create_response(500, error_details)