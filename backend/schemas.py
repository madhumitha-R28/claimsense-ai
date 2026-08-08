from pydantic import BaseModel, Field


class ClaimCreate(BaseModel):
    policy_number: str
    claim_amount: float = Field(gt=0)
    hospital_name: str
    diagnosis: str


class UserCreate(BaseModel):
    username: str
    password: str


class ClaimProcess(BaseModel):
    claim_amount: float
    diagnosis: str