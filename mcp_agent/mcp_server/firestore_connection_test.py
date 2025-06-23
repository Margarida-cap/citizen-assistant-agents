from google.cloud import firestore
from google.oauth2 import service_account
import time

credentials = service_account.Credentials.from_service_account_file("../hacker2025-team-38-dev-556d08c6be6a.json")
db = firestore.Client(credentials=credentials, database="mcp-test")

start = time.time()
collections = [col.id for col in db.collections()]
print(f"Collections: {collections}")
print(f"Took {time.time()-start} seconds")


doc = db.collection("Users").document('5atiOSaVrXg31L5zTX9oF5mLHZx2').get()
print(f"Document: {doc.id} - {doc.to_dict() if doc.exists else 'Not found'}")


