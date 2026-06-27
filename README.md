# AI Travel Planner Agent

An AI-powered travel planning app built with Streamlit. It helps users generate a travel itinerary, view weather information, discover transport options, and get hotel suggestions based on their trip details. The app also includes a travel-guidelines assistant powered by a RAG pipeline.

## Features

- Generate a trip itinerary from source, destination, days, and budget
- Show current weather for the destination
- Suggest transport options (flights, buses, trains)
- Recommend hotels based on the destination and budget
- Answer travel-related questions using a retrieval-augmented generation (RAG) assistant
- Use free public APIs for transport, hotel, and weather data where possible

## Project Structure

```text
.
├── app.py                      # Streamlit web application entry point
├── planner_agent.py            # Main planner logic that orchestrates itinerary generation
├── weather.py                  # Weather lookup using Open-Meteo
├── transport.py                # Transport lookup using OpenStreetMap data
├── hotel.py                    # Hotel lookup using OpenStreetMap data
├── rag/                        # RAG components for travel guidelines
│   ├── loader.py
│   ├── rag_qa.py
│   ├── rag_store.py
│   └── retriever.py
├── prompts/                    # Prompt templates for the planner and agents
├── langgraph_flow/             # LangGraph workflow components
├── tools/                      # Tool modules and registry
├── api/                        # FastAPI-related files (kept for extension or future use)
├── data/                       # Travel guideline data and supporting files
├── faiss_index/                # Vector index for RAG
├── tests/                      # Unit tests
├── requirements.txt            # Python dependencies
└── .env                        # Local environment variables (not committed)
```

## Requirements

- Python 3.10+
- Streamlit
- LangChain
- Google Gemini API access
- Internet access for external API lookups

## Installation

1. Clone the repository
2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

On Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with your Gemini API key

```env
GOOGLE_API_KEY=your_google_gemini_api_key
```

## Running the App

Start the Streamlit app:

```bash
streamlit run app.py
```

Then open the local URL shown by Streamlit in your browser.

## Testing

Run the available tests:

```bash
python -m unittest discover -s tests -p "test_real_api_sources.py"
```

## Deployment Notes

For deployment on Streamlit Cloud or similar platforms:

- Add the `GOOGLE_API_KEY` as a secret/environment variable
- Ensure the app can access the required data files and index folder
- Keep the app self-contained so it can run without a separate FastAPI backend

## Notes

- The app uses public APIs for weather, transport, and hotels when available.
- If those services are unavailable or rate-limited, the app falls back to sensible default values so the experience remains usable.
- The RAG assistant depends on the data and vector index stored under the `data/` and `faiss_index/` folders.
