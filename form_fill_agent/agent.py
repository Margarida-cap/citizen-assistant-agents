import os

from google.adk import Agent
from tavily import TavilyClient
# from google.adk.tools.langchain_tool import LangchainTool # import
# from google.adk.agents.callback_context import CallbackContext

#from langchain.tools.tavily_search import TavilySearchResults  search engine for agents
from dotenv import load_dotenv


from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

from google.adk.tools import ToolContext

# 1. Load environment variables from the agent directory's .env file
load_dotenv()
model_name = os.getenv("MODEL")



from google.adk.tools import ToolContext, FunctionTool
from google.genai import types

############################################################
############################################################
############################################################

# For file artifact

def get_document_fields(
    document_name: str, tool_context: ToolContext
) -> dict:
    """
    Extracts fillable field names from a government PDF form using pypdf.

    Args:
        document_name (str): The name of the document artifact to analyze.

    Returns:
        dict: {
            "status": "success",
            "fields": ["field1", "field2", ...]
        }
    """
    import requests
    import tempfile
    from pypdf import PdfReader
    # 1. Load the artifact
    try:
        print(f"Tool: Attempting to load artifact: {document_name}")
        document_part = tool_context.load_artifact(document_name)

        if not document_part:
            return {"status": "error", "message": f"Document '{document_name}' not found."}
        print(f"Tool: Successfully loaded artifact: {document_part}")
        reader = PdfReader(document_part)
        form_fields = reader.get_fields()

        if not form_fields:
            return {"status": "error", "error_message": "No fillable fields found in the PDF."}

        field_names = list(form_fields.keys())
        return {"status": "success", "fields": field_names}

    except Exception as e:
        return {"status": "error", "error_message": str(e)}


def fill_pdf_form_file(document_name: str, user_data: dict, tool_context: ToolContext):
    """
    Fills a government PDF form using provided user data and pypdf.

    Args:
        pdf_url (str): The URL to the blank PDF form.
        user_data (dict): A dictionary of {field_name: value}.

    Returns:
        dict: {
            "status": "success",
            "filled_pdf_path": "/mnt/data/filled_form.pdf"
        }
    """
    import requests
    import tempfile
    import os
    from pypdf import PdfReader, PdfWriter

    try:

        print(f"Tool: Attempting to load artifact: {document_name}")
        document_part = tool_context.load_artifact(document_name)

        if not document_part:
            return {"status": "error", "message": f"Document '{document_name}' not found."}
        print(f"Tool: Successfully loaded artifact: {document_part}")
        reader = PdfReader(document_part)
        writer = PdfWriter()
        writer.append(reader)

        first_page = writer.pages[0]
        writer.update_page_form_field_values(first_page, user_data, auto_regenerate=False)

        output_path = "/mnt/data/filled_form.pdf"
        with open(output_path, "wb") as output_stream:
            writer.write(output_stream)

        return {"status": "success", "filled_pdf_path": output_path}

    except Exception as e:
        return {"status": "error", "error_message": str(e)}



############################################################
############################################################
############################################################

# For URL



def extract_pdf_form_fields(pdf_url: str, tool_context: ToolContext):
    """
    Extracts fillable field names from a government PDF form using pypdf.

    Args:
        pdf_url (str): The URL to the PDF form.

    Returns:
        dict: {
            "status": "success",
            "fields": ["field1", "field2", ...]
        }
    """
    import requests
    import tempfile
    from pypdf import PdfReader

    try:
        response = requests.get(pdf_url)
        response.raise_for_status()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(response.content)
            tmp_file_path = tmp_file.name

        reader = PdfReader(tmp_file_path)
        form_fields = reader.get_fields()

        if not form_fields:
            return {"status": "error", "error_message": "No fillable fields found in the PDF."}

        field_names = list(form_fields.keys())
        return {"status": "success", "fields": field_names}

    except Exception as e:
        return {"status": "error", "error_message": str(e)}

def fill_pdf_form(pdf_url: str, user_data: dict):
    """
    Fills a government PDF form using provided user data and pypdf.

    Args:
        pdf_url (str): The URL to the blank PDF form.
        user_data (dict): A dictionary of {field_name: value}.

    Returns:
        dict: {
            "status": "success",
            "filled_pdf_path": "filled_ds82.pdf"
        }
    """
    import requests
    import tempfile
    import os
    from pypdf import PdfReader, PdfWriter

    try:
        response = requests.get(pdf_url)
        response.raise_for_status()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(response.content)
            tmp_file_path = tmp_file.name

        reader = PdfReader(tmp_file_path)
        writer = PdfWriter()
        writer.append(reader)

        # Iterate over all pages and update form fields on each page
        for page in writer.pages:
            writer.update_page_form_field_values(page, user_data, auto_regenerate=False)

        output_path = "filled_form.pdf"
        with open(output_path, "wb") as output_stream:
            writer.write(output_stream)

        return {"status": "success", "filled_pdf_path": output_path}

    except Exception as e:
        return {"status": "error", "error_message": str(e)}




# root_agent = Agent(
#     name="form_fill_agent",
#     model=model_name,
#     description=("Help users fill forms for governmental services."),
#     instruction=(instruction),
#         tools=[]
# )

############################3## For PDF URL
# root_agent = Agent(
#     name="form_fill_agent",
#     model=model_name,
#     description="Help users fill out government PDF forms.",
#     instruction="""
    
#         When the user provides a pdf form, call the extract_pdf_form_fields tool first
#         to understand what information is needed. 
#         Then, based on the extracted fields, ask the user for any missing data.
#         Once all necessary data is collected, call the fill_pdf_form to fill the form.
    
#         The user information is the following:
#         - Full Name: John Doe
#         - Date of Birth: 01/01/1990 
#         - Address: 123 Main St, Springfield, IL
#         - Email: johndoe@gmail.com 
#         - Phone Number: +1-555-123-4567
#         - Social Security Number: 123-45-6789
#     """,
#     tools=[extract_pdf_form_fields, fill_pdf_form]
# # )
# def save_uploaded_file(file_content_base64: str, filename: str, tool_context: ToolContext):
#     """
#     Saves an uploaded file as an artifact.

#     Args:
#         file_content_base64 (str): The base64-encoded content of the uploaded file.
#         filename (str): The name to save the file as.
#         tool_context (ToolContext): The tool context for artifact management.

#     Returns:
#         dict: {
#             "status": "success",
#             "artifact_name": filename
#         }
#     """
#     import base64
#     try:
#         file_content = base64.b64decode(file_content_base64)
#         artifact_name = filename
#         tool_context.save_artifact(file_content, artifact_name)
#         return {"status": "success", "artifact_name": artifact_name}
#     except Exception as e:
#         return {"status": "error", "error_message": str(e)}

root_agent = Agent(
    name="form_fill_agent",
    model=model_name,
    description="Help users fill out government PDF forms.",
    instruction="""
    
        When the user provides a pdf form url call the `extract_pdf_form_fields` tool 
        to understand what information is needed. 
        Then, based on the extracted fields, ask the user for any missing data.
        Then create a dictionary with field names as keys and the user data as value.
        Print this dictionary to the user so they can review it, in JSON format.
        Use this data with the `fill_pdf_form` tool to fill the form.
        The user information is the following:
        - Full Name: John Doe
        - Date of Birth: 01/01/1990 
        - Address: 123 Main St, Springfield, IL
        - Email: johndoe@gmail.com 
        - Phone Number: +1-555-123-4567
        - Social Security Number: 123-45-6789
    """,
    tools=[extract_pdf_form_fields, fill_pdf_form]
)


