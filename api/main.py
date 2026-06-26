from fastapi import FastAPI
from api.schemas import TripRequest
from planner_agent import generate_itinerary

app = FastAPI(
    title="Travel Agent API",
    version="1.0"
)


@app.get('/')
def home():
    return {"message":"Travel planner API is running"}

@app.post("/generate-trip")
def generate_trip(request:TripRequest):
    result = generate_itinerary(
        request.source,
        request.destination,
        request.days,
        request.budget
    )
    return result