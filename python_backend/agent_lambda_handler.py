# agent_lambda_handler.py
import json
import traceback
from typing import Any, Dict
from decimal import Decimal

from agent_service import AgentService

class DecimalEncoder(json.JSONEncoder):
    """Custom JSON encoder to handle Decimal types"""
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return super(DecimalEncoder, self).default(obj)

def create_response(status_code: int, body: Any) -> Dict[str, Any]:
    """Create a response with CORS headers"""
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

def handler(event, context):
    print("Lambda invoked with event:", json.dumps(event))

    # Handle OPTIONS requests for CORS preflight
    if event.get('httpMethod') == 'OPTIONS':
        print("Handling OPTIONS request")
        return create_response(200, {
            'message': 'CORS preflight handled successfully'
        })

    try:
        print(f"Received event: {json.dumps(event)}")
        
        # Parse path to determine action
        path = event.get('path', '').rstrip('/').split('/')[-1]
        print(f"Processing path: {path}")

        # Parse request body
        body = {}
        if event.get('body'):
            try:
                body = json.loads(event.get('body'))
            except json.JSONDecodeError:
                return create_response(400, {'message': 'Invalid JSON in request body'})

        agent_service = AgentService()

        # Handle getProperties separately without requiring agentId
        if path == 'getProperties':
            result = agent_service.get_properties()
            return create_response(200, result)

        # Only check for root-level agentId for endpoints that need it
        if path in ['getAgent', 'getAppointments', 'getClients', 'getTransactions', 'getOffice']:
            agent_id = body.get('agentId')
            if not agent_id:
                return create_response(400, {'message': 'agentId is required'})

            # Route to appropriate handler based on path
            if path == 'getAgent':
                result = agent_service.get_agent(agent_id)
                if result is None:
                    return create_response(404, {'message': 'Agent not found'})
                return create_response(200, result)

            elif path == 'getAppointments':
                result = agent_service.get_appointments(agent_id)
                return create_response(200, result)

            elif path == 'getClients':
                result = agent_service.get_clients(agent_id)
                return create_response(200, result)

            elif path == 'getTransactions':
                result = agent_service.get_transactions(agent_id)
                return create_response(200, result)

            elif path == 'getOffice':
                result = agent_service.get_office(agent_id)
                if result is None:
                    return create_response(404, {'message': 'Office not found'})
                return create_response(200, result)

        elif path == 'addProperty':
            if not body.get('property'):
                print("No property object in request body")
                return create_response(400, {'message': 'Property data is required'})
            
            property_data = body['property']
            print(f"Processing property data: {json.dumps(property_data)}")

            required_fields = [
                'agentId', 'propertyType', 'street', 'city', 'state', 'zipcode',
                'listPrice', 'numBedrooms', 'numBathrooms', 'squareFootage',
                'description', 'status', 'imageUrl', 'listingDate'
            ]
            
            missing_fields = [field for field in required_fields if not property_data.get(field)]
            if missing_fields:
                print(f"Missing required fields: {missing_fields}")
                return create_response(400, {
                    'message': 'Missing required fields',
                    'fields': missing_fields,
                    'received_fields': list(property_data.keys())
                })

            # Type validation
            try:
                property_data['listPrice'] = Decimal(str(property_data['listPrice']))
                property_data['numBedrooms'] = int(property_data['numBedrooms'])
                property_data['numBathrooms'] = int(property_data['numBathrooms'])
                property_data['squareFootage'] = int(property_data['squareFootage'])
            except (ValueError, TypeError) as e:
                print(f"Type conversion error: {str(e)}")
                return create_response(400, {
                    'message': 'Invalid numeric value',
                    'error': str(e)
                })

            try:
                property_id = agent_service.add_property(property_data)
                return create_response(200, {'propertyId': property_id})
            except ValueError as ve:
                print(f"Validation error: {str(ve)}")
                return create_response(400, {'message': str(ve)})

        elif path == 'addTransaction':
            print(f"Processing addTransaction with data: {json.dumps(body)}")
            required_fields = ['agentId', 'clientId', 'propertyId', 'amount', 'transactionType', 'dateSent']
            
            missing_fields = [field for field in required_fields if not body.get(field)]
            if missing_fields:
                print(f"Missing required fields: {missing_fields}")
                return create_response(400, {
                    'message': 'Missing required fields',
                    'fields': missing_fields,
                    'received_fields': list(body.keys())
                })

            try:
                body['amount'] = Decimal(str(body['amount']))
                
                # Validate transaction type
                valid_types = ['SALE', 'PURCHASE', 'RENTAL']
                if body['transactionType'] not in valid_types:
                    return create_response(400, {
                        'message': f'Invalid transaction type. Must be one of: {", ".join(valid_types)}'
                    })

                transaction_id = agent_service.add_transaction(body)
                return create_response(200, {'transactionId': transaction_id})
            except ValueError as ve:
                print(f"Validation error: {str(ve)}")
                return create_response(400, {'message': str(ve)})

        else:
            return create_response(400, {'message': f'Unknown path: {path}'})

    except json.JSONDecodeError:
        return create_response(400, {'message': 'Invalid JSON in request body'})
    except Exception as e:
        print(f"Error: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return create_response(500, {
            'message': 'Internal server error',
            'error': str(e),
            'type': e.__class__.__name__
        })