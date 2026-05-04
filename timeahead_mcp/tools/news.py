from timeahead_mcp import client


def get_latest_news(category: str = "", source: str = "", limit: int = 10) -> list[dict]:
    """
    Get the latest AI and technology news from timeahead's aggregator.

    Pulls from 48+ curated sources updated hourly. Each article includes
    title, excerpt, source name, published date, URL, and tags.

    Args:
        category: Filter by category (e.g. "AI News", "Research"). Leave blank for all.
        source: Filter by source name (e.g. "The Verge"). Leave blank for all.
        limit: Number of articles (1-30, default 10).
    """
    params: dict = {'limit': limit}
    if category:
        params['category'] = category
    if source:
        params['source'] = source
    return client.get('news/', params)


def search_news(query: str, limit: int = 10) -> list[dict]:
    """
    Search AI and technology news articles by keyword.

    Searches article titles and excerpts across all 48+ sources.

    Args:
        query: Search keyword or phrase.
        limit: Number of results (1-30, default 10).
    """
    return client.get('news/search/', {'query': query, 'limit': limit})


def get_digest(digest_type: str = "top-this-week") -> dict:
    """
    Get a curated digest of MCP servers.

    Available digest types:
      - top-this-week        : 10 highest-scored servers
      - most-downloaded      : 10 most-downloaded servers this week
      - new-arrivals         : 10 most recently discovered servers
      - worst-security       : servers with detected secrets/credentials
      - security-regressions : servers whose score dropped most recently

    Args:
        digest_type: One of the five types listed above (default "top-this-week").
    """
    return client.get(f'digest/{digest_type}/')
