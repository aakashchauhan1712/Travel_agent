from fastapi import FastAPI

from schemas import TripRequest, TripResponse

from agent_executor import run_agent

app = FastAPI()


@app.get("/")
def home():
    return {"message": "AI Travel Planner API Running"}


@app.post("/generate-trip", response_model=TripResponse)
def generate_trip(request: TripRequest):

    query = f"""
Plan a {request.days} day trip.

Source: {request.source}

Destination: {request.destination}

Budget: ₹{request.budget}

Include transportation, weather, hotels and itinerary.
"""

    answer = run_agent(query)

    return TripResponse(
        answer=answer
    )