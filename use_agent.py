from vertexai import agent_engines
from vertexai.preview.reasoning_engines import AdkApp


adk_app = agent_engines.get(
    "projects/421799929445/locations/us-central1/reasoningEngines/4989592562940510208"
)

session = adk_app.create_session(user_id="kishore_1")
print("session:", session)
print("session id:", session["id"])


print("\nStarting stream_query …")
try:
    for ev in adk_app.stream_query(
        user_id="kishore_1",
        session_id=session["id"],
        message="What’s the weather in New York today?",
    ):
        print(type(ev).__name__, getattr(ev, "text", ev))
except Exception as e:
    print("Error during streaming:", e)

print("stream_query finished.")
