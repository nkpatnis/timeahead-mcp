from timeahead_mcp import client


def recommend_for_task(task: str, min_score: int = 60, limit: int = 3) -> list[dict]:
    """
    Recommend MCP servers for a described task or use case.

    Matches the task description against server names, descriptions, and tags
    using keyword matching. Returns servers above min_score, ordered by trust
    score, each with a why_recommended explanation.

    Examples:
      - "I need to read and write files on disk"
      - "Query a Postgres database"
      - "Post messages to Slack and read GitHub issues"

    Args:
        task: Natural language description of what you need the MCP to do.
        min_score: Minimum trust score for recommendations (default 60).
        limit: Number of recommendations (1-10, default 3).
    """
    return client.get('recommend/', {'task': task, 'min_score': min_score, 'limit': limit})


def recommend_safer_alternative(slug: str, limit: int = 3) -> dict:
    """
    Find safer, higher-scored alternatives to a given MCP server.

    Returns the original server's score for comparison, then up to N
    alternatives that cover similar functionality but score higher.
    Each alternative includes an "improvement" string quantifying the gain.

    Use this when a server has a low score or the user asks for a safer option.

    Args:
        slug: The slug of the server to find alternatives for.
        limit: Number of alternatives to return (1-5, default 3).
    """
    return client.get(f'alternative/{slug}/', {'limit': limit})
