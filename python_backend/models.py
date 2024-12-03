from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Transaction:
    transaction_id: str
    property_id: str
    agent_id: str
    client_id: str
    date_sent: str
    amount: float
    transaction_type: str

    @classmethod
    def from_dynamodb(cls, item: dict) -> Optional['Transaction']:
        if not item:
            return None
        return cls(
            transaction_id=item.get('transactionId'),
            property_id=item.get('propertyId'),
            agent_id=item.get('agentId'),
            client_id=item.get('clientId'),
            date_sent=item.get('dateSent'),
            amount=item.get('amount'),
            transaction_type=item.get('transactionType')
        )

    def to_dict(self) -> dict:
        return {
            'transactionId': self.transaction_id,
            'propertyId': self.property_id,
            'agentId': self.agent_id,
            'clientId': self.client_id,
            'dateSent': self.date_sent,
            'amount': self.amount,
            'transactionType': self.transaction_type
        }

@dataclass
class Property:
    property_id: str
    agent_id: str
    property_type: str
    street: str
    city: str
    state: str
    zipcode: str
    list_price: float
    num_bedrooms: int
    num_bathrooms: int
    square_footage: int
    description: str
    listing_date: str
    status: str
    image_url: str

    @classmethod
    def from_dynamodb(cls, item: dict) -> Optional['Property']:
        if not item:
            return None
        return cls(
            property_id=item.get('propertyId'),
            agent_id=item.get('agentId'),
            property_type=item.get('propertyType'),
            street=item.get('street'),
            city=item.get('city'),
            state=item.get('state'),
            zipcode=item.get('zipcode'),
            list_price=item.get('listPrice'),
            num_bedrooms=item.get('numBedrooms'),
            num_bathrooms=item.get('numBathrooms'),
            square_footage=item.get('squareFootage'),
            description=item.get('description'),
            listing_date=item.get('listingDate'),
            status=item.get('status'),
            image_url=item.get('imageUrl')
        )

    def to_dict(self) -> dict:
        return {
            'propertyId': self.property_id,
            'agentId': self.agent_id,
            'propertyType': self.property_type,
            'street': self.street,
            'city': self.city,
            'state': self.state,
            'zipcode': self.zipcode,
            'listPrice': self.list_price,
            'numBedrooms': self.num_bedrooms,
            'numBathrooms': self.num_bathrooms,
            'squareFootage': self.square_footage,
            'description': self.description,
            'listingDate': self.listing_date,
            'status': self.status,
            'imageUrl': self.image_url
        }

@dataclass
class Office:
    office_id: str
    office_name: str
    street: str
    city: str
    state: str
    zipcode: str
    phone: str

    @classmethod
    def from_dynamodb(cls, item: dict) -> Optional['Office']:
        if not item:
            return None
        return cls(
            office_id=item.get('officeId'),
            office_name=item.get('officeName'),
            street=item.get('street'),
            city=item.get('city'),
            state=item.get('state'),
            zipcode=item.get('zipcode'),
            phone=item.get('phone')
        )

    def to_dict(self) -> dict:
        return {
            'officeId': self.office_id,
            'officeName': self.office_name,
            'street': self.street,
            'city': self.city,
            'state': self.state,
            'zipcode': self.zipcode,
            'phone': self.phone
        }