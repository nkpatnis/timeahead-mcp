[![MCPScore](https://timeahead.in/api/v1/mcp/badge/timeahead-mcp.svg)](https://timeahead.in/mcp/timeahead-mcp)

# timeahead-mcp

MCP server for [timeahead.in](https://timeahead.in) — live, independent trust scores for MCP servers.

timeahead scores 800+ MCP servers nightly across five dimensions: security (35%), freshness (25%), adoption (20%), quality (10%), and trust (10%). This package gives any AI assistant (Claude Desktop, Cursor, Cline, Continue) direct access to those scores so it can answer questions like "which Postgres MCP is safest?" with live data instead of stale training.

---

## Install

```bash
# One-time global install
uvx timeahead-mcp

# Or add to mcp.json
{
  "mcpServers": {
    "timeahead": {
      "command": "uvx",
      "args": ["timeahead-mcp"],
      "env": {
        "TIMEAHEAD_API_KEY": "ta_mcp_..."
      }
    }
  }
}
```

The `TIMEAHEAD_API_KEY` is optional. Without it you get 200 requests/hour (anonymous). Get a free key at [timeahead.in](https://timeahead.in) for 500 req/hr.

---

## Tools

### Discovery

| Tool | Description |
|---|---|
| `search_servers` | Search by keyword. Filters: registry, min_score, risk_class. |
| `list_categories` | All 16 tracked categories (postgres, github, slack, etc.) with counts. |
| `get_new_servers` | Servers discovered in the last N days. |
| `get_trending` | Most-downloaded servers this week. |

### Trust & Inspection

| Tool | Description |
|---|---|
| `get_score` | Full 0-100 score with per-dimension breakdown and human-readable notes. |
| `get_findings` | Security findings, capability flags, maintenance health, install result. |
| `get_server_detail` | Everything in one call: score + findings + install command. |
| `compare_servers` | Side-by-side comparison of 2-5 servers with a rule-based recommendation. |

### Risk & History

| Tool | Description |
|---|---|
| `get_score_history` | Score trend over N days (improving / stable / declining). |
| `get_score_drops` | Servers whose score dropped most in the last N days. |
| `audit_my_stack` | Audit all servers in your mcp.json. Returns aggregate risk, per-server action (keep/review/replace), and a plain-English summary. |

### Recommendations

| Tool | Description |
|---|---|
| `recommend_for_task` | "I need to read GitHub issues and post Slack messages" → top-scored servers that match. |
| `recommend_safer_alternative` | Given a low-scored server, returns higher-scored alternatives covering the same domain. |

### AI News Feed

| Tool | Description |
|---|---|
| `get_latest_news` | Latest articles from 48+ AI and tech sources. Filter by category or source. |
| `search_news` | Keyword search across all articles. |
| `get_digest` | Curated digests: top-this-week, most-downloaded, new-arrivals, worst-security, security-regressions. |

---

## Example prompts

```
"Which Postgres MCP server should I install?"
→ search_servers("postgres", min_score=70)

"Is my current MCP setup safe? Here are my installed servers: [slugs]"
→ audit_my_stack([...])

"What changed in MCP security this week?"
→ get_score_drops(days=7)

"Find me a safer alternative to filesystem-mcp"
→ recommend_safer_alternative("filesystem-mcp")

"Should I use mcp-server-postgres or mcp-postgres-pro?"
→ compare_servers(["mcp-server-postgres", "mcp-postgres-pro"])

"What's happening in AI this week?"
→ get_latest_news(limit=5)
```

---

## Environment variables

| Variable | Default | Description |
|---|---|---|
| `TIMEAHEAD_BASE_URL` | `https://timeahead.in` | Backend URL (change for self-hosted) |
| `TIMEAHEAD_API_KEY` | _(empty)_ | Optional API key for higher rate limits |
| `TIMEAHEAD_TIMEOUT` | `15` | HTTP timeout in seconds |

---

## Scoring methodology

Scores are computed nightly by scanning each server's repository (Gitleaks for secrets, AST analysis for capability flags), fetching GitHub maintenance metrics, and checking weekly download counts from npm/PyPI.

timeahead's own MCP server is scored on the same rubric with no special treatment. [View the methodology](https://timeahead.in/about#scoring).

---

## License

MIT — see [LICENSE](LICENSE).
