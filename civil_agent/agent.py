import os
import time
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

from google.adk import Agent
from google.adk.sessions import InMemorySessionService
from google.adk.events import Event, EventActions
from google.adk.tools import ToolContext
from tavily import TavilyClient
from civil_agent.validators import *

__all__ = ["root_agent", "runner", "session"]



from google.adk.runners import Runner

from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters



session_service = InMemorySessionService()
session = session_service.create_session(app_name="citizen-assistant", user_id="user1")



# Load environment variables
load_dotenv()
model_name = os.getenv("MODEL")
tavily_key = os.getenv("TAVILY_API_KEY")

# Initialize Tavily client
client = TavilyClient(api_key=tavily_key)

# Initialize session service
# session_service = InMemorySessionService()

# ------------------- TOOL 1 -------------------
def search_government_info(query: str):
    """
    Searches for a government webpage relevant to the query using Tavily.

    Args:
        query (str): The user's query or question.

    Returns:
        dict: {
            "status": "success",
            "url": "...",
            "title": "...",
            "content": "..."
        }
        or
        {"status": "error", "error_message": "..."}
    """
    try:
        r = client.search(query, include_domains=["*.gov"], max_results=5)
        results = r.get("results", [])
        if results:
            first = results[0]
            return {
                "status": "success",
                "url": first["url"],
                "title": first["title"],
                "content": first["content"]
            }
        return {"status": "error", "error_message": "No gov URL found."}
    except Exception as e:
        return {"status": "error", "error_message": str(e)}

# ------------------- TOOL 2 -------------------
def scrape_government_page(url: str, tool_context: ToolContext):
    """
    Scrapes a government webpage and returns its readable content and internal links.

    Args:
        url (str): The full URL of the government page to scrape.
        tool_context (ToolContext): Contains session state for tracking visited URLs.

    Returns:
        dict: {"status": "success", "content": "...", "links": {"[Link Text]": "[URL]", ...}}
    """
    visited = tool_context.state.get("visited_urls", [])
    if url in visited:
        return {"status": "error", "error_message": "URL already visited in this session."}
    visited.append(url)
    tool_context.state["visited_urls"] = visited

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Clean HTML
        for tag in soup(["script", "style", "nav", "footer", "noscript", "header", "aside", "form"]):
            tag.decompose()

        content = soup.get_text(separator="\n", strip=True)
        lines = [line.strip() for line in content.splitlines() if line.strip()]
        full_text = "\n".join(lines)

        # Extract links with text
        links = {}
        for a in soup.find_all("a", href=True):
            text = a.get_text(strip=True)
            href = a["href"].strip()
            if text:
                full_url = urljoin(url, href)
                if ".gov" in full_url and full_url not in links:
                    links[text] = full_url


        # Add links to session state
        scraped_links = tool_context.state.get("scraped_links", [])
        for link_text, link_url in links.items():
            if link_url not in scraped_links:
                scraped_links.append(link_url)
        tool_context.state["scraped_links"] = scraped_links
        
        return {
            "status": "success",
            "content": full_text[:20000],  # Cap content length
            "links": links
        }

    except Exception as e:
        return {"status": "error", "error_message": str(e)}





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











instruction=("""
Assist users with questions about U.S. government services such as renewing passports, applying for visas, or obtaining permits.
Use search_government_info to find the most relevant .gov page.
Then use scrape_government_page to extract readable content and links.
Store the links in session state as scraped_links, and track visited pages in visited_urls.
If the answer is not complete, inspect scraped_links and choose a relevant link to follow by calling scrape_government_page again.

Always include the URLs used to retrieve the information in your final response.
Avoid revisiting URLs already in visited_urls.

When the user provides or requests to change any personal data field, the agent must run the corresponding validate_<field> function before accepting or updating that value.
For example, if the user says “Change my sex to Male,” call validate_sex("Male") to confirm it's valid; if it fails, prompt the user to correct it. 
Apply the same pattern for all fields (e.g. validate_date_of_birth, validate_ssn, validate_email, etc.), and only proceed once each input passes validation.

If the user asks for help filling a form, say this ability is in testing. Then, show how it would work using the DS82 form - passport renewal form.
For this, first give the user the url https://storage.googleapis.com/demo-for-files/ds82_blank_form.pdf and call the extract_pdf_form_fields tool with this link to get the fields of the form.
Then, use the MCP get_user_information tool to fetch the user data with the user id 5atiOSaVrXg31L5zTX9oF5mLHZx2.
Based on the extracted fields, ask the user for any missing data. Then create a dictionary with field names as keys and the user data as values. Show the dictionary to the user. 
With all necessary data collected, fill the form by calling the fill_pdf_form tool. Notify the user that the filled form is available for download.     
                         

""")
# If the user provided additional information, ask the user if they want to add this information to their profile.
# If they agree use the MCP `add_user_information` tool to update the user data in the database.





script_dir = os.path.dirname(os.path.abspath(__file__))
relative_path = os.path.join(script_dir, "mcp_server", "server.py")
print(f"Using script: {relative_path}")
    




# ------------------- AGENT -------------------
root_agent = Agent(
    name="civil_agent",
    model=model_name,
    description="Help users find official government information like renewing passports or applying for visas.",
    instruction=instruction,
    tools=[
        search_government_info,
        scrape_government_page,
        
        MCPToolset(
            connection_params=StdioServerParameters(
                command="uv",
                args=["run", "--with", "mcp", "mcp", "run", relative_path]
            )
        ),
        extract_pdf_form_fields,
        fill_pdf_form,

        # validators tools
        validate_sex,
        validate_birth_place,
        validate_country,
        validate_other_names,
        validate_document_type,
        validate_height,
        validate_hair_color,
        validate_eye_color,
        validate_occupation,
        validate_employer,
        validate_phone_number,
        validate_email,
        validate_ssn,
        validate_date_of_birth,
        validate_full_name,
        validate_address,


    ]
)
 #---------------------------RUNNER---------------------------

runner = Runner(
  agent=root_agent,                # your LlmAgent or Agent instance
  app_name="citizen-assistant",               # must match your session’s app_name
  session_service=session_service  # the service you just created
)