from timeahead_mcp import client


def get_score(slug: str) -> dict:
    """
    Get the full trust score breakdown for an MCP server.

    Returns a 0-100 composite score split across five dimensions:
    security (35%), freshness (25%), adoption (20%), quality (10%), trust (10%).
    Each dimension includes a human-readable note explaining the score.

    Also returns risk_class (low/medium/high), whether secrets were detected
    in the repository, and a link to the full listing.

    Args:
        slug: The server's slug (e.g. "mcp-server-postgres").
    """
    return client.get(f'score/{slug}/')


def get_findings(slug: str) -> dict:
    """
    Get detailed security findings and capability analysis for an MCP server.

    Returns what the server can actually do (reads filesystem, makes network
    calls, spawns processes, uses eval, requires API keys), maintenance health
    (CI status, bus factor, release cadence), and the last sandboxed install
    attempt result.

    Use this when you need to explain WHY a server has a certain risk profile.

    Args:
        slug: The server's slug.
    """
    return client.get(f'findings/{slug}/')


def get_server_detail(slug: str) -> dict:
    """
    Get the complete profile for an MCP server in one call.

    Merges score breakdown, security findings, capability analysis,
    maintenance metrics, install info, and vendor claim status.
    Includes install_command for immediate use.

    Use this when you need everything about a specific server.

    Args:
        slug: The server's slug.
    """
    return client.get(f'detail/{slug}/')


def compare_servers(slugs: list[str]) -> dict:
    """
    Compare 2-5 MCP servers side by side.

    Returns all five score dimensions for each server plus a rule-based
    recommendation (highest score, no secrets detected, low risk wins).

    Use this to answer "should I use X or Y?" questions.

    Args:
        slugs: List of 2-5 server slugs to compare.
    """
    if len(slugs) < 2:
        return {'error': 'Provide at least 2 slugs to compare.'}
    if len(slugs) > 5:
        return {'error': 'Maximum 5 slugs per comparison.'}
    return client.get('compare/', {'slugs': ','.join(slugs)})
