from vertexai import agent_engines
from vertexai.preview.reasoning_engines import AdkApp


adk_app = agent_engines.get(
    "projects/421799929445/locations/us-central1/reasoningEngines/4989592562940510208"
)

session = adk_app.create_session(user_id="kishore_1")


import json

print("\nStarting stream_query …")
try:
    for ev in adk_app.stream_query(
        user_id="kishore_1",
        session_id=session["id"],
        message="What’s the weather in New York today?",
    ):
        if isinstance(ev, dict):  # older SDK, raw dicts
            content = ev.get("content", {}).get("parts", [])
            if "function_call" in content[0]:
                call = content[0]["function_call"]
                print(f"\n🔧 Tool Call: {call['name']}({json.dumps(call['args'])})")

            elif "function_response" in content[0]:
                response = content[0]["function_response"]
                print(f"\n✅ Tool Result from {response['name']}:")
                print(json.dumps(response["response"], indent=2))

            elif "text" in content[0]:
                print(f"\n💬 Final Agent Response:\n{content[0]['text'].strip()}")

        else:  # newer SDKs with typed events
            from vertexai.preview.reasoning_engines.types import ToolCall, ToolResult, LlmResponse
            if isinstance(ev, ToolCall):
                print(f"\n🔧 Tool Call: {ev.name}({ev.args})")
            elif isinstance(ev, ToolResult):
                print(f"\n✅ Tool Result from {ev.name}:\n{json.dumps(ev.response, indent=2)}")
            elif isinstance(ev, LlmResponse):
                print(f"\n💬 Final Agent Response:\n{ev.text.strip()}")
            else:
                print(f"Unknown event type: {ev}")
except Exception as e:
    print("❌ Error during streaming:", e)

print("\nstream_query finished.")

