import os
from google.cloud import firestore
from google.oauth2 import service_account

from mcp.server.fastmcp import FastMCP
from mcp.server.sse import SseServerTransport
from mcp.shared.exceptions import McpError
from mcp.types import ErrorData, INTERNAL_ERROR, INVALID_PARAMS

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.routing import Route, Mount
from starlette.responses import JSONResponse

# Load credentials and initialize client
credentials = service_account.Credentials.from_service_account_file("../hacker2025-team-38-dev-556d08c6be6a.json")
db = firestore.Client(credentials=credentials)

# Create MCP server
mcp = FastMCP("gcp-firestore")

@mcp.tool()
def get_firestore_document(collection: str, doc_id: str) -> dict:
    """Fetch a document from Google Cloud Firestore (NOT Firebase)."""
    try:
        doc_ref = db.collection(collection).document(doc_id)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            raise McpError(ErrorData(code=INVALID_PARAMS, message="Document not found."))
    except Exception as e:
        raise McpError(ErrorData(code=INTERNAL_ERROR, message=str(e)))

# Optional tool to list docs
@mcp.tool()
def list_firestore_documents(collection: str, limit: int = 5) -> list:
    """List document IDs from a collection."""
    try:
        docs = db.collection(collection).limit(limit).stream()
        return [doc.id for doc in docs]
    except Exception as e:
        raise McpError(ErrorData(code=INTERNAL_ERROR, message=str(e)))

# SSE support
sse = SseServerTransport("/messages/")

async def handle_sse(request: Request):
    _server = mcp._mcp_server
    async with sse.connect_sse(request.scope, request.receive, request._send) as (reader, writer):
        await _server.run(reader, writer, _server.create_initialization_options())

# Optional ping route
async def ping(request: Request):
    return JSONResponse({"status": "ok"})

# Starlette app
app = Starlette(
    debug=True,
    routes=[
        Route("/ping", ping),
        Route("/sse", endpoint=handle_sse),
        Mount("/messages/", app=sse.handle_post_message),
    ]
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8001)
