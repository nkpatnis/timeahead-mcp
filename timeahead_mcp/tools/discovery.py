from timeahead_mcp import client


def search_servers(
    query: str,
    registry: str = "",
    min_score: int = 0,
    risk_class: str = "",
    limit: int = 10,
) -> list[dict]:
    """
    Search MCP servers by keyword.

    Returns servers ranked by trust score. Each result includes the slug,
    name, composite score (0-100), grade (A-F), risk class, install command,
    and a direct link to the listing.

    Args:
        query: Keyword to search (matches name, description, tags).
        registry: Filter by "npm", "pypi", or "github". Leave blank for all.
        min_score: Minimum composite score (0-100). Default 0 = no filter.
        risk_class: Filter by "low", "medium", or "high". Leave blank for all.
        limit: Number of results to return (1-50, default 10).
    """
    params = {'query': query, 'limit': limit}
    if registry:
        params['registry'] = registry
    if min_score:
        params['min_score'] = min_score
    if risk_class:
        params['risk_class'] = risk_class
    return client.get('search/', params)


def list_categories() -> list[dict]:
    """
    List all MCP server categories tracked by timeahead.

    Returns 16 categories (postgres, github, slack, database, etc.)
    with server counts, top score, and the top-ranked server slug.
    Useful for understanding what domains are covered before searching.
    """
    return client.get('categories/')


def get_new_servers(days: int = 7, limit: int = 10) -> list[dict]:
    """
    Get recently discovered MCP servers.

    Args:
        days: Look back window (1-30 days, default 7).
        limit: Number of results (1-50, default 10).
    """
    return client.get('new/', {'days': days, 'limit': limit})


def get_trending(limit: int = 10) -> list[dict]:
    """
    Get the most-downloaded MCP servers this week.

    Ordered by weekly download count. Useful for understanding what
    the community is actually using.

    Args:
        limit: Number of results (1-50, default 10).
    """
    return client.get('trending/', {'limit': limit})
