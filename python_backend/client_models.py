from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Client:
    client_id: str
    first_name: str
    last_name: str
    email: str
    phone: str
    street: str
    city: str
    state: str
    zipcode: str

    @classmethod
    def from_dynamodb(cls, item: dict) -> Optional['Client']:
        if not item:
            return None
        return cls(
            client_id=item.get('clientId'),
            first_name=item.get('firstName'),
            last_name=item.get('lastName'),
            email=item.get('email'),
            phone=item.get('phone'),
            street=item.get('street'),
            city=item.get('city'),
            state=item.get('state'),
            zipcode=item.get('zipcode')
        )

    def to_dict(self) -> dict:
        return {
            'clientId': self.client_id,
            'firstName': self.first_name,
            'lastName': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'street': self.street,
            'city': self.city,
            'state': self.state,
            'zipcode': self.zipcode
        }

@dataclass
class ClientAgent:
    id: str
    client_id: str
    agent_id: str
    relationship_date: str
    status: str = "ACTIVE"

    @classmethod
    def create_relationship(cls, client_id: str, agent_id: str) -> 'ClientAgent':
        return cls(
            id=f"{client_id}#{agent_id}",
            client_id=client_id,
            agent_id=agent_id,
            relationship_date=datetime.now().isoformat(),
            status="ACTIVE"
        )

    @classmethod
    def from_dynamodb(cls, item: dict) -> Optional['ClientAgent']:
        if not item:
            return None
        return cls(
            id=item.get('id'),
            client_id=item.get('clientId'),
            agent_id=item.get('agentId'),
            relationship_date=item.get('relationshipDate'),
            status=item.get('status', 'ACTIVE')
        )

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'clientId': self.client_id,
            'agentId': self.agent_id,
            'relationshipDate': self.relationship_date,
            'status': self.status
        }

    @staticmethod
    def generate_id(client_id: str, agent_id: str) -> str:
        return f"{client_id}#{agent_id}"

@dataclass
class Appointment:
    appointment_id: str
    client_id: str
    agent_id: str
    property_id: str
    appointment_date: str
    appointment_time: str
    purpose: str

    @classmethod
    def from_dynamodb(cls, item: dict) -> Optional['Appointment']:
        if not item:
            return None
        return cls(
            appointment_id=item.get('appointmentId'),
            client_id=item.get('clientId'),
            agent_id=item.get('agentId'),
            property_id=item.get('propertyId'),
            appointment_date=item.get('appointmentDate'),
            appointment_time=item.get('appointmentTime'),
            purpose=item.get('purpose')
        )

    def to_dict(self) -> dict:
        return {
            'appointmentId': self.appointment_id,
            'clientId': self.client_id,
            'agentId': self.agent_id,
            'propertyId': self.property_id,
            'appointmentDate': self.appointment_date,
            'appointmentTime': self.appointment_time,
            'purpose': self.purpose
        }