from dotenv import load_dotenv
from ddgs import DDGS
from trafilatura import fetch_url, extract
from pydantic import BaseModel
from crewai.tools import tool
load_dotenv()



class WebScraper(BaseModel):
    query: str
    result_title: str
    result_url: str
    body: str
    data: str


@tool("Live Stock Information Tool")
def web_searcher(query: str) -> WebScraper:
    """
    Search the web for a given query and extract content from
    the first accessible search result.

    Args:
        query (str): The topic or question to search for.

    Returns:
        WebScraper: A structured object containing the search query,
        result title, source URL, search snippet, and extracted
        webpage data in JSON format.

    Note:
        Searches for one result and skips webpages that cannot
        be downloaded. Returns no result if no accessible webpage
        is found.
    """


    results = DDGS().text(
        query,
        region="in-en",
        max_results=1,
    )

    for result in results:
        download = fetch_url(result.get("href"), )
        if download is None:
            continue

        data = extract(download, output_format="json", with_metadata=True) or ""
        return WebScraper(
            query=query,
            result_title=result.get("title"),
            result_url=result.get("href"),
            body=result.get("body"),
            data=data,
        )

    raise RuntimeError(f"No accessible search result found for query: {query}")
