from pydantic import BaseModel, ConfigDict, EmailStr


class ClientCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str | None = None


class ClientResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str | None = None
    advisor_id: int

    model_config = ConfigDict(from_attributes=True)