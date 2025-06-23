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
tavily_key = os.getenv("TAVILY_API_KEY")

print(f"Using key: {tavily_key}")

# Initialize Tavily client
client = TavilyClient(api_key=tavily_key)
# ------------------- TOOL 1 -------------------
def find_government_url(query: str):
    """
    Searches for a government webpage relevant to the query using Tavily.

    Args:
        query (str): The user's query or question.

    Returns:
        dict: {
            "status": "success",
            "url": "...",
            "title": "...",
            "summary": "..."
        }
        or
        {"status": "error", "error_message": "..."}
    """
    try:
        r = client.search(query, include_domains=["*.gov"], max_results=5)
        results = r.get("results", [])
        if results:
            first = results[0]
            print(first)
            return {
                "status": "success",
                "url": first["url"],
                "title": first["title"],
                "summary": first["content"]
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
        dict: {"status": "success", "content": "...", "links": {"Link Text": "URL", ...}}
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

        return {
            "status": "success",
            "content": full_text[:8000],  # Cap content length
            "links": links
        }

    except Exception as e:
        return {"status": "error", "error_message": str(e)}


# ------------------- TOOL 3 -------------------
def follow_government_link(link_text: str, from_links: dict, tool_context: ToolContext):
    """
    Scrapes the content of a link selected from a previous government page's link list.

    Args:
        link_text (str): The anchor text of the link to follow.
        from_links (dict): Dictionary of {"Link Text": "URL"} from the previous page.
        tool_context (ToolContext): Contains session state for tracking visited URLs.

    Returns:
        dict: {"status": "success", "content": "..."} or error info
    """
    if link_text not in from_links:
        return {"status": "error", "error_message": "Link text not found in provided links."}

    url = from_links[link_text]
    return scrape_government_page(url, tool_context)




root_agent = Agent(
    name="civil_agent",
    model=model_name,
    description=("Help users find official government information like renewing passports or applying for visas."),
    instruction=("""
        Assist users with questions about U.S. government services such as renewing passports, applying for visas, or obtaining permits.
        Use the search_government_info tool to find the most relevant .gov page.
        Then use scrape_government_page to extract readable content and links.
        If the answer is not complete, follow up using scrape_related_link.
        Avoid repeating links and keep track of visited URLs.

        Previously visited pages: {{ visited_urls? }}
        """),
        tools=[find_government_url, scrape_government_page, follow_government_link]
)



