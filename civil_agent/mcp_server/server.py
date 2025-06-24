from mcp.server.fastmcp import FastMCP
from google.cloud import firestore
from google.oauth2 import service_account
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from google.adk.sessions import InMemorySessionService
from google.oauth2 import id_token
from google.auth.transport import requests as grequests





from google.genai import types
from civil_agent.agent import runner, session_service

load_dotenv()

CLIENT_ID = "299771489297-hv6h409jk0se5ubn5bdmnajmnffibhdi.apps.googleusercontent.com"

credentials_name = "hacker2025-team-38-dev-556d08c6be6a.json"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
credentials_path = os.path.join(BASE_DIR, credentials_name)
print("Credentials path:", credentials_path)

credentials = service_account.Credentials.from_service_account_file(credentials_path)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
db = firestore.Client(credentials=credentials, database="mcp-test")

mcp = FastMCP("Firestore MCP", enable_inspector=True)

@mcp.tool()
def get_user_information(user_id: str) -> dict:
    print("Fetching infromation for user with id: ", user_id)
    doc = db.collection("Users").document(user_id).get()
    if doc.exists:
        return doc.to_dict()
    else:
        return {"error": f"No user found with ID {user_id}"}
    

@mcp.tool()
def add_user_information(user_id: str, parameters_to_add : dict) -> dict:
    print("Updating information for user with id: ", user_id)
    # Add or update user information in Firestore
    try:
        db.collection("Users").document(user_id).set(parameters_to_add, merge=True)
    except Exception as e:
        return {"error": f"Failed to add user information: {str(e)}"}    

# --- FastAPI wrapper for frontend integration ---
app = FastAPI()

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def verify_google_token(token):
    try:
        idinfo = id_token.verify_oauth2_token(token, grequests.Request(), CLIENT_ID)
        return idinfo  # contains user info
    except Exception:
        return None

@app.post("/messages/")
async def messages(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token")
    token = auth_header.split(" ")[1]
    user_info = verify_google_token(token)
    if not user_info:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    data = await request.json()
    user_query = data.get("user_query")
    if not user_query:
        return {"error": "No user_query provided"}

    return {"reply": f"Echo: {user_query} (user: {user_info.get('email')})"} #just to test frontend
    session_obj = await session_service.create_session(app_name="citizen-assistant", user_id="user1")

    # Wrap the user’s text into a Content object
    content = types.Content(
        role="user",
        parts=[types.Part(text=user_query)]
    )

    # Stream events from the Runner
    final_reply = ""
    async for event in runner.run_async(
        user_id=session_obj.user_id,
        session_id=session_obj.id,
        new_message=content
    ):
        # When the Runner emits the final LLM response, capture it
        if event.is_final_response() and event.content and event.content.parts:
            final_reply = event.content.parts[0].text

    return {"reply": final_reply}



    # Here you can call your agent logic, or for demo, just echo:
    # If you want to use MCP tools, you need to route the query accordingly.
    # For now, just return a dummy response:
    #return {"reply": f"Echo: {user_query}"}

# Optionally, expose MCP's ASGI app at another route if needed
# app.mount("/mcp", mcp)

if __name__ == "__main__":
    mcp.run(transport="stdio")