"""
timeahead MCP server entry point.

Registers all 15 tools and runs the server using stdio transport
(compatible with Claude Desktop, Cursor, Cline, Continue, and any
MCP client that supports the stdio transport).

Usage:
  uvx timeahead-mcp           # anonymous, 200 req/hr limit
  TIMEAHEAD_API_KEY=ta_mcp_... uvx timeahead-mcp   # keyed, higher limits
"""

from mcp.server.fastmcp import FastMCP

from timeahead_mcp.tools.discovery import (
    get_new_servers,
    get_trending,
    list_categories,
    search_servers,
)
from timeahead_mcp.tools.news import get_digest, get_latest_news, search_news
from timeahead_mcp.tools.recommendations import (
    recommend_for_task,
    recommend_safer_alternative,
)
from timeahead_mcp.tools.risk import audit_my_stack, get_score_drops, get_score_history
from timeahead_mcp.tools.trust import (
    compare_servers,
    get_findings,
    get_score,
    get_server_detail,
)

mcp = FastMCP(
    "timeahead",
    instructions=(
        "timeahead provides live, independent trust scores for MCP servers — "
        "scored nightly on security (35%), freshness (25%), adoption (20%), "
        "quality (10%), and trust (10%). "
        "Key workflows: "
        "1. Finding a server → search_servers or recommend_for_task. "
        "2. Evaluating one server → get_score then get_findings if needed. "
        "3. Comparing options → compare_servers. "
        "4. Auditing installed servers → audit_my_stack (pass slugs from mcp.json). "
        "5. Monitoring changes → get_score_drops or get_score_history. "
        "6. AI news → get_latest_news or search_news. "
        "Every response includes a listing_url linking back to timeahead.in."
    ),
)

# Group A — Discovery
mcp.tool()(search_servers)
mcp.tool()(list_categories)
mcp.tool()(get_new_servers)
mcp.tool()(get_trending)

# Group B — Trust & Inspection
mcp.tool()(get_score)
mcp.tool()(get_findings)
mcp.tool()(get_server_detail)
mcp.tool()(compare_servers)

# Group C — Risk & History
mcp.tool()(get_score_history)
mcp.tool()(get_score_drops)
mcp.tool()(audit_my_stack)

# Group D — Recommendations
mcp.tool()(recommend_for_task)
mcp.tool()(recommend_safer_alternative)

# Group E — News Feed
mcp.tool()(get_latest_news)
mcp.tool()(search_news)
mcp.tool()(get_digest)


def main() -> None:
    mcp.run(transport='stdio')


if __name__ == '__main__':
    main()
