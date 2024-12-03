from dataclasses import dataclass
from typing import Optional
from boto3.dynamodb.conditions import Key

@dataclass
class Agent:
    agent_id: str
    office_id: str
    first_name: str
    last_name: str
    email: str
    phone: str
    license_number: str
    date_hired: str

    @classmethod
    def from_dynamodb(cls, item: dict) -> Optional['Agent']:
        if not item:
            return None
        return cls(
            agent_id=item.get('agentId'),
            office_id=item.get('officeId'),
            first_name=item.get('firstName'),
            last_name=item.get('lastName'),
            email=item.get('email'),
            phone=item.get('phone'),
            license_number=item.get('licenseNumber'),
            date_hired=item.get('dateHired')
        )

    def to_dict(self) -> dict:
        return {
            'agentId': self.agent_id,
            'officeId': self.office_id,
            'firstName': self.first_name,
            'lastName': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'licenseNumber': self.license_number,
            'dateHired': self.date_hired
        }
