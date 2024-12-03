from typing import Optional, List, Dict, Any
import uuid
from datetime import datetime
from boto3.dynamodb.conditions import Key

class PropertyService:
    def __init__(self, dynamodb_resource):
        self.dynamodb = dynamodb_resource
        self.table = self.dynamodb.Table('dev-Property')

    def add_property(self, property_data: Dict[str, Any]) -> str:
        property_data['propertyId'] = str(uuid.uuid4())
        property_data['listingDate'] = datetime.now().isoformat()
        self.table.put_item(Item=property_data)
        return property_data['propertyId']

    def get_property(self, property_id: str) -> Optional[Dict[str, Any]]:
        response = self.table.get_item(Key={'propertyId': property_id})
        return response.get('Item')

class TransactionService:
    def __init__(self, dynamodb_resource):
        self.dynamodb = dynamodb_resource
        self.table = self.dynamodb.Table('dev-Transaction')

    def add_transaction(self, transaction_data: Dict[str, Any]) -> str:
        transaction_data['transactionId'] = str(uuid.uuid4())
        self.table.put_item(Item=transaction_data)
        return transaction_data['transactionId']

    def get_transactions_by_agent(self, agent_id: str) -> List[Dict[str, Any]]:
        response = self.table.query(
            IndexName='agent-index',
            KeyConditionExpression=Key('agentId').eq(agent_id)
        )
        return response.get('Items', [])