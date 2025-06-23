from vertexai import agent_engines

agent = agent_engines.get("projects/299771489297/locations/us-central1/reasoningEngines/6147668578058371072")

# Required parameters
user_id = "your_user_id"
message = "What is your function?"

# stream_query returns a generator (stream of responses)
for response in agent.stream_query(user_id=user_id, message=message):
    print(response)