"""
Deploys `root_agent` to Vertex AI Agent Engine.

Required env vars:
  PROJECT_ID, LOCATION, STAGING_BUCKET
"""

import os
import vertexai
from vertexai import agent_engines
from weather_agent.agent import root_agent
from vertexai.preview import reasoning_engines
from dotenv import load_dotenv

load_dotenv()


vertexai.init(
    project=os.environ["PROJECT_ID"],
    location=os.environ.get("LOCATION", "us-central1"),
    staging_bucket=os.environ["STAGING_BUCKET"],
)

app = reasoning_engines.AdkApp(
    agent=root_agent,    
    enable_tracing=True,
)


remote_app = agent_engines.create(
    agent_engine=app,
    extra_packages=["weather_agent"],
    requirements=["google-cloud-aiplatform[adk,agent_engines]"],
)


# agent_engines.delete(resource_name="projects/421799929445/locations/us-central1/reasoningEngines/4989592562940510208", force=True)