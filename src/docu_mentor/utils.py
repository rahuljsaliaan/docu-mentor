import requests
import tldextract
import time
from typing import List
from urllib.parse import urlparse
from http import HTTPStatus
from firecrawl import FirecrawlApp, ScrapeOptions
from langchain_core.documents import Document

from docu_mentor.core import settings


def is_valid_url(url: str) -> bool:
    """Checks if the URL is well-formed and accessible."""

    try:
        result = urlparse(url)
        is_valid_url = all([result.scheme in ("http", "https"), result.netloc])

        if not is_valid_url:
            return False

        # Check if the URL is accessible
        return is_accessible_url(url)
    except:
        return False


def is_accessible_url(url: str) -> bool:
    """Checks if the URL is reachable and responds with a status code of 200."""

    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        return response.status_code == HTTPStatus.OK
    except requests.RequestException:
        return False


def get_main_doc_name_from_url(url: str) -> str:
    # Parse the URL
    parsed_url = urlparse(url)

    # Use tldextract to extract the domain name parts
    extracted = tldextract.extract(parsed_url.netloc)

    # The domain part is in extracted.domain (ignoring subdomains and TLDs)
    return extracted.domain


def custom_firecrawl_loader(
    url: str, limit: int = 10, only_main_content: bool = True
) -> List[Document]:
    client = FirecrawlApp(api_key=settings.api.firecrawl_api_key)

    # Start the crawl job
    response = client.crawl_url(
        url=url,
        limit=limit,
        scrape_options=ScrapeOptions(
            formats=["markdown"], onlyMainContent=only_main_content
        ),
        poll_interval=30,
    )

    # Poll for the crawl job to complete
    if not response.success:
        raise Exception(f"Failed to crawl URL: {url}")

    # Retrieve the crawled data
    data = response.data
    documents = []

    for page in data:
        page.links
        content = page.markdown
        metadata = page.metadata

        documents.append(Document(page_content=content, metadata=metadata))

    return documents
