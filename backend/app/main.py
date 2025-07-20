from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from vertexai import agent_engines
import json, os

origins = [
    "https://digiker-test-1.s3.us-west-2.amazonaws.com",  # your frontend
    "http://localhost:8000",  # optional: for local dev
]

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


ENGINE_ID = (
    "projects/421799929445/locations/us-central1/reasoningEngines/2065349029893505024"
)
_adk_app = None  # cache


def get_adk_app():
    global _adk_app
    if _adk_app is None:
        _adk_app = agent_engines.get(ENGINE_ID)
    return _adk_app


@app.get("/")
def root():
    return {"message": "Hello from Cloud Run"}


@app.post("/chat")
async def chat(request: Request):
    body = await request.json()
    message = body["message"]
    adk_app = get_adk_app()
    session = adk_app.create_session(user_id="anonymous")

    async def stream():
        for ev in adk_app.stream_query(
            user_id="anonymous",
            session_id=session["id"],
            message=message,
        ):
            yield json.dumps(ev) + "\n"

    return StreamingResponse(stream(), media_type="application/x-ndjson")
