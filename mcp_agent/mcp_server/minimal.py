from mcp.server.fastmcp import FastMCP
from google.cloud import firestore
from google.oauth2 import service_account
import os


# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# os.chdir(BASE_DIR)
# print("Current working directory:", BASE_DIR)

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

app = mcp

if __name__ == "__main__":
    mcp.run(transport="stdio") 