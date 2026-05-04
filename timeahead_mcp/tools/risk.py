from timeahead_mcp import client


def get_score_history(slug: str, days: int = 30) -> dict:
    """
    Get the score trend for an MCP server over time.

    Returns a list of score snapshots with all five sub-dimensions,
    plus a trend label (improving / stable / declining) and the net
    score delta over the window.

    Args:
        slug: The server's slug.
        days: History window in days (1-90, default 30).
    """
    return client.get(f'history/{slug}/', {'days': days})


def get_score_drops(days: int = 7, min_drop: int = 5, limit: int = 20) -> list[dict]:
    """
    Get MCP servers whose trust score dropped recently.

    Compares each server's current score against its score N days ago.
    Useful for security monitoring: "what changed in MCP security this week?"

    Args:
        days: Look-back window (1-30 days, default 7).
        min_drop: Minimum score drop to include (default 5 points).
        limit: Maximum results (1-50, default 20).
    """
    return client.get('drops/', {'days': days, 'min_drop': min_drop, 'limit': limit})


def audit_my_stack(slugs: list[str]) -> dict:
    """
    Audit a set of installed MCP servers for security risks.

    Pass the slugs of all MCP servers in your mcp.json. Returns:
    - aggregate_risk: overall risk level (low / medium / high)
    - overall_score: average composite score
    - per-server action: keep / review / replace
    - weakest_link: the most problematic server with a plain-English reason
    - summary: a 1-2 sentence human-readable verdict

    This is the highest-value tool. Use it whenever a user pastes their
    mcp.json or asks "is my MCP setup safe?"

    Args:
        slugs: List of MCP server slugs (up to 20).
    """
    if not slugs:
        return {'error': 'Provide at least one slug.'}
    if len(slugs) > 20:
        return {'error': 'Maximum 20 servers per audit.'}
    return client.get('audit/', {'slugs': ','.join(slugs)})
