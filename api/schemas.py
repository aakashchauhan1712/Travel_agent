from pydantic import BaseModel


class TripRequest(BaseModel):
    source: str
    destination: str
    days: int
    budget: int