from typing import Optional
from pydantic import BaseModel, Field, EmailStr, field_validator, model_validator
import json

class Address(BaseModel):
    city: str = Field(..., min_length=2)
    street: str = Field(..., min_length=3)
    house_number: int = Field(..., gt=0)

class User(BaseModel):
    name: str = Field(..., min_length=2)
    age: int = Field(..., ge=0, le=120)
    email: EmailStr
    is_employed: bool
    address: Address

    @field_validator('name')
    def name_must_be_letters(cls, v):
        if not v.replace(' ', '').isalpha():
            raise ValueError('Name must contain only letters and spaces')
        return v

    @model_validator(mode='after')
    def check_employment_age(self):
        if self.is_employed and not (18 <= self.age <= 65):
            raise ValueError('If employed, age must be between 18 and 65')
        return self

def process_registration(json_str: str) -> str:
    try:
        data = json.loads(json_str)
        user = User(**data)
        return user.model_dump_json(indent=4)
    except Exception as e:
        return f'Validation Error: {str(e)}'

valid_json = """
{
    "name": "John Doe",
    "age": 30,
    "email": "john.doe@example.com",
    "is_employed": true,
    "address": {
        "city": "New York",
        "street": "5th Avenue",
        "house_number": 123
    }
}
"""

invalid_json_age = """
{
    "name": "John Doe",
    "age": 70,
    "email": "john.doe@example.com",
    "is_employed": true,
    "address": {
        "city": "New York",
        "street": "5th Avenue",
        "house_number": 123
    }
}
"""

invalid_json_name = """
{
    "name": "John123",
    "age": 25,
    "email": "john.doe@example.com",
    "is_employed": false,
    "address": {
        "city": "NY",
        "street": "5th Avenue",
        "house_number": 123
    }
}
"""

if __name__ == "__main__":
    print("=== VALID JSON ===")
    print(process_registration(valid_json))
    print("\n=== INVALID JSON (age too high for employment) ===")
    print(process_registration(invalid_json_age))
    print("\n=== INVALID JSON (name with digits) ===")
    print(process_registration(invalid_json_name))
