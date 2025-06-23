import os
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

from google.adk import Agent
from google.adk.tools import ToolContext
from tavily import TavilyClient

# Load environment variables
load_dotenv()
model_name = os.getenv("MODEL")
tavily_key = os.getenv("TAVILY_API_KEY")

print(f"Using key: {tavily_key}")

# Initialize Tavily client
client = TavilyClient(api_key=tavily_key)

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
        dict: {
            "status": "success",
            "content": "...",
            "links": {"Link Text": "URL", ...}
        }
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

        for tag in soup(["script", "style", "nav", "footer", "noscript", "header", "aside", "form"]):
            tag.decompose()

        content = soup.get_text(separator="\n", strip=True)
        lines = [line.strip() for line in content.splitlines() if line.strip()]
        full_text = "\n".join(lines)

        links = {}
        for a in soup.find_all("a", href=True):
            text = a.get_text(strip=True)
            href = a["href"].strip()
            if text:
                full_url = urljoin(url, href)
                if ".gov" in full_url and full_url not in links:
                    links[text] = full_url

        tool_context.state["scraped_links"] = links

        return {
            "status": "success",
            "content": full_text[:8000],
            "links": links
        }

    except Exception as e:
        return {"status": "error", "error_message": str(e)}

# ------------------- TOOL 3 -------------------
def follow_government_link(link_text: str, tool_context: ToolContext):
    """
    Follows a selected link from the previously scraped government page and scrapes its content.

    Args:
        link_text (str): The anchor text of the link to follow.
        tool_context (ToolContext): Contains session state including scraped links and visited URLs.

    Returns:
        dict: {
            "status": "success",
            "content": "..."
        } or error info
    """
    from_links = tool_context.state.get("scraped_links", {})
    if link_text not in from_links:
        return {"status": "error", "error_message": "Link text not found in stored links."}

    url = from_links[link_text]
    return scrape_government_page(url, tool_context)

# ------------------- TOOL 4 -------------------
def analyze_links_for_relevance(query: str, tool_context: ToolContext):
    """
    Analyzes the stored links from the last scraped page and returns those most relevant to the query.

    Args:
        query (str): The user's original question or topic.
        tool_context (ToolContext): Contains session state including scraped links.

    Returns:
        dict: {
            "status": "success",
            "relevant_links": {"Link Text": "URL", ...}
        }
    """
    links = tool_context.state.get("scraped_links", {})
    if not links:
        return {"status": "error", "error_message": "No links available to analyze."}

    relevant = {text: url for text, url in links.items() if query.lower() in text.lower()}
    return {"status": "success", "relevant_links": relevant}

# ------------------- AGENT -------------------
root_agent = Agent(
    name="civil_agent",
    model=model_name,
    description="Help users find official government information like renewing passports or applying for visas.",
    instruction=("""
        Assist users with questions about U.S. government services such as renewing passports, applying for visas, or obtaining permits.
        Use `search_government_info` to find the most relevant .gov page.
        Then use `scrape_government_page` to extract readable content and links.
        Store the links in session state as `scraped_links`.
        If the information gathered is not enough to answer the user's question, inspect `scraped_links` and decide which link to follow using `follow_government_link`.
        You may use `analyze_links_for_relevance` to help identify useful links.
        Always include the URLs used to retrieve the information in your final response.
        Avoid repeating links and keep track of visited URLs in `visited_urls`.
    """),
    tools=[
        search_government_info,
        scrape_government_page,
        follow_government_link,
        analyze_links_for_relevance
    ]
)
