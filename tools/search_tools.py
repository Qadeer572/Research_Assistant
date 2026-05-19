"""
search_tools.py
LangChain-compatible tool wrappers for Tavily, ArXiv, and NewsAPI.
Each function can be used standalone or registered as a LangChain Tool.
"""
import logging
from typing import List, Dict, Any
from config.settings import get_settings
settings = get_settings()

logger = logging.getLogger(__name__)


# ── Tavily Web Search ──────────────────────────────────────────────────────────

def tavily_search(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """
    Search the web via Tavily API.
    Replace the placeholder body with the real Tavily client call.
    """
    logger.info("[tavily_search] Query: %s", query)

    # ── Real implementation (uncomment when TAVILY_API_KEY is set) ───────────
    # from tavily import TavilyClient
    # client = TavilyClient(api_key=settings.TAVILY_API_KEY)
    # response = client.search(query=query, max_results=max_results)
    # return [
    #     {
    #         "title": r.get("title", ""),
    #         "url": r.get("url", ""),
    #         "content": r.get("content", ""),
    #         "source_type": "web",
    #         "metadata": {},
    #     }
    #     for r in response.get("results", [])
    # ]

    return [
        {
            "title": f"[Tavily Placeholder] {query}",
            "url": "https://example.com/tavily-result",
            "content": f"Placeholder Tavily content for query: {query}",
            "source_type": "web",
            "metadata": {},
        }
    ]


# ── ArXiv Academic Search ──────────────────────────────────────────────────────

def arxiv_search(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """
    Search academic papers via the ArXiv API.
    Replace the placeholder body with the real arxiv client call.
    """
    logger.info("[arxiv_search] Query: %s", query)

    # ── Real implementation (uncomment after: pip install arxiv) ─────────────
    # import arxiv
    # search = arxiv.Search(query=query, max_results=max_results, sort_by=arxiv.SortCriterion.Relevance)
    # return [
    #     {
    #         "title": paper.title,
    #         "url": paper.entry_id,
    #         "content": paper.summary,
    #         "source_type": "arxiv",
    #         "metadata": {
    #             "authors": [str(a) for a in paper.authors],
    #             "published": str(paper.published),
    #         },
    #     }
    #     for paper in search.results()
    # ]

    return [
        {
            "title": f"[ArXiv Placeholder] Paper on {query}",
            "url": "https://arxiv.org/abs/placeholder",
            "content": f"Placeholder abstract for ArXiv query: {query}",
            "source_type": "arxiv",
            "metadata": {"authors": ["Author A, Author B"], "published": "2024-01-01"},
        }
    ]


# ── NewsAPI Search ─────────────────────────────────────────────────────────────

def newsapi_search(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """
    Search recent news articles via NewsAPI.
    Replace the placeholder body with the real newsapi-python client call.
    """
    logger.info("[newsapi_search] Query: %s", query)

    # ── Real implementation (uncomment after: pip install newsapi-python) ────
    # from newsapi import NewsApiClient
    # client = NewsApiClient(api_key=settings.NEWSAPI_KEY)
    # response = client.get_everything(q=query, language="en", page_size=max_results)
    # return [
    #     {
    #         "title": a.get("title", ""),
    #         "url": a.get("url", ""),
    #         "content": a.get("description", ""),
    #         "source_type": "news",
    #         "metadata": {
    #             "published_at": a.get("publishedAt", ""),
    #             "source": a.get("source", {}).get("name", ""),
    #         },
    #     }
    #     for a in response.get("articles", [])
    # ]

    return [
        {
            "title": f"[NewsAPI Placeholder] Article on {query}",
            "url": "https://news.example.com/article",
            "content": f"Placeholder news content for query: {query}",
            "source_type": "news",
            "metadata": {"published_at": "2024-06-01", "source": "Example News"},
        }
    ]
