"""
Tool tests using respx to mock the HTTP layer.
All tests verify input validation and response pass-through — they do not
test Django business logic (that lives in the backend test suite).
"""

import respx
import httpx
import pytest

from timeahead_mcp.tools.discovery import search_servers, list_categories, get_new_servers, get_trending
from timeahead_mcp.tools.trust import get_score, get_findings, get_server_detail, compare_servers
from timeahead_mcp.tools.risk import get_score_history, get_score_drops, audit_my_stack
from timeahead_mcp.tools.recommendations import recommend_for_task, recommend_safer_alternative
from timeahead_mcp.tools.news import get_latest_news, search_news, get_digest

BASE = 'https://timeahead.in/mcp/v1'

_SUMMARY = {
    'slug': 'mcp-server-postgres',
    'name': 'MCP Server Postgres',
    'score': 74.0,
    'grade': 'B',
    'risk_class': 'low',
    'secrets_found': False,
    'weekly_downloads': 4200,
    'install_command': 'npx mcp-server-postgres',
    'listing_url': 'https://timeahead.in/mcp/mcp-server-postgres',
}


# ---------------------------------------------------------------------------
# Group A — Discovery
# ---------------------------------------------------------------------------

@respx.mock
def test_search_servers_basic():
    respx.get(f'{BASE}/search/').mock(return_value=httpx.Response(200, json=[_SUMMARY]))
    result = search_servers(query='postgres')
    assert isinstance(result, list)
    assert result[0]['slug'] == 'mcp-server-postgres'


@respx.mock
def test_search_servers_with_filters():
    respx.get(f'{BASE}/search/').mock(return_value=httpx.Response(200, json=[_SUMMARY]))
    result = search_servers(query='postgres', registry='npm', min_score=70, risk_class='low', limit=5)
    assert isinstance(result, list)


@respx.mock
def test_list_categories():
    payload = [{'slug': 'postgres', 'title': 'Best MCP for PostgreSQL', 'server_count': 8}]
    respx.get(f'{BASE}/categories/').mock(return_value=httpx.Response(200, json=payload))
    result = list_categories()
    assert isinstance(result, list)
    assert result[0]['slug'] == 'postgres'


@respx.mock
def test_get_new_servers():
    respx.get(f'{BASE}/new/').mock(return_value=httpx.Response(200, json=[_SUMMARY]))
    result = get_new_servers(days=7, limit=5)
    assert isinstance(result, list)


@respx.mock
def test_get_trending():
    respx.get(f'{BASE}/trending/').mock(return_value=httpx.Response(200, json=[_SUMMARY]))
    result = get_trending(limit=5)
    assert isinstance(result, list)


# ---------------------------------------------------------------------------
# Group B — Trust & Inspection
# ---------------------------------------------------------------------------

@respx.mock
def test_get_score():
    payload = {'slug': 'mcp-server-postgres', 'score': 74, 'grade': 'B', 'breakdown': {}}
    respx.get(f'{BASE}/score/mcp-server-postgres/').mock(return_value=httpx.Response(200, json=payload))
    result = get_score('mcp-server-postgres')
    assert result['slug'] == 'mcp-server-postgres'
    assert result['grade'] == 'B'


@respx.mock
def test_get_findings():
    payload = {'slug': 'mcp-server-postgres', 'risk_class': 'low', 'capabilities': {}}
    respx.get(f'{BASE}/findings/mcp-server-postgres/').mock(return_value=httpx.Response(200, json=payload))
    result = get_findings('mcp-server-postgres')
    assert result['risk_class'] == 'low'


@respx.mock
def test_get_server_detail():
    payload = {'slug': 'mcp-server-postgres', 'name': 'MCP Server Postgres', 'score': {}}
    respx.get(f'{BASE}/detail/mcp-server-postgres/').mock(return_value=httpx.Response(200, json=payload))
    result = get_server_detail('mcp-server-postgres')
    assert result['slug'] == 'mcp-server-postgres'


@respx.mock
def test_compare_servers():
    payload = {'servers': [_SUMMARY, _SUMMARY], 'recommendation': {'best_slug': 'mcp-server-postgres'}}
    respx.get(f'{BASE}/compare/').mock(return_value=httpx.Response(200, json=payload))
    result = compare_servers(['mcp-server-postgres', 'another-server'])
    assert 'recommendation' in result


def test_compare_servers_too_few():
    result = compare_servers(['only-one'])
    assert 'error' in result


def test_compare_servers_too_many():
    result = compare_servers(['a', 'b', 'c', 'd', 'e', 'f'])
    assert 'error' in result


# ---------------------------------------------------------------------------
# Group C — Risk & History
# ---------------------------------------------------------------------------

@respx.mock
def test_get_score_history():
    payload = {'slug': 'mcp-server-postgres', 'trend': 'stable', 'snapshots': []}
    respx.get(f'{BASE}/history/mcp-server-postgres/').mock(return_value=httpx.Response(200, json=payload))
    result = get_score_history('mcp-server-postgres', days=30)
    assert result['trend'] == 'stable'


@respx.mock
def test_get_score_drops():
    respx.get(f'{BASE}/drops/').mock(return_value=httpx.Response(200, json=[]))
    result = get_score_drops(days=7, min_drop=5)
    assert isinstance(result, list)


@respx.mock
def test_audit_my_stack():
    payload = {
        'aggregate_risk': 'low',
        'overall_score': 74.0,
        'servers_audited': 1,
        'servers': [],
        'summary': 'Your stack looks good.',
    }
    respx.get(f'{BASE}/audit/').mock(return_value=httpx.Response(200, json=payload))
    result = audit_my_stack(['mcp-server-postgres'])
    assert result['aggregate_risk'] == 'low'


def test_audit_empty_slugs():
    result = audit_my_stack([])
    assert 'error' in result


def test_audit_too_many_slugs():
    result = audit_my_stack([f'slug-{i}' for i in range(21)])
    assert 'error' in result


# ---------------------------------------------------------------------------
# Group D — Recommendations
# ---------------------------------------------------------------------------

@respx.mock
def test_recommend_for_task():
    respx.get(f'{BASE}/recommend/').mock(return_value=httpx.Response(200, json=[_SUMMARY]))
    result = recommend_for_task(task='query postgres database')
    assert isinstance(result, list)


@respx.mock
def test_recommend_safer_alternative():
    payload = {'original': _SUMMARY, 'alternatives': [_SUMMARY]}
    respx.get(f'{BASE}/alternative/bad-server/').mock(return_value=httpx.Response(200, json=payload))
    result = recommend_safer_alternative('bad-server')
    assert 'alternatives' in result


# ---------------------------------------------------------------------------
# Group E — News Feed
# ---------------------------------------------------------------------------

@respx.mock
def test_get_latest_news():
    payload = [{'title': 'AI news', 'excerpt': 'Something happened', 'url': 'https://example.com'}]
    respx.get(f'{BASE}/news/').mock(return_value=httpx.Response(200, json=payload))
    result = get_latest_news(limit=5)
    assert isinstance(result, list)
    assert result[0]['title'] == 'AI news'


@respx.mock
def test_search_news():
    payload = [{'title': 'Claude news', 'url': 'https://example.com'}]
    respx.get(f'{BASE}/news/search/').mock(return_value=httpx.Response(200, json=payload))
    result = search_news(query='claude')
    assert isinstance(result, list)


@respx.mock
def test_get_digest():
    payload = {'digest_type': 'top-this-week', 'title': 'Top 10', 'servers': [_SUMMARY]}
    respx.get(f'{BASE}/digest/top-this-week/').mock(return_value=httpx.Response(200, json=payload))
    result = get_digest('top-this-week')
    assert result['digest_type'] == 'top-this-week'


# ---------------------------------------------------------------------------
# Error handling
# ---------------------------------------------------------------------------

@respx.mock
def test_http_error_returns_error_dict():
    respx.get(f'{BASE}/score/nonexistent/').mock(return_value=httpx.Response(404, json={'detail': 'Not found'}))
    result = get_score('nonexistent')
    assert 'error' in result


@respx.mock
def test_network_error_returns_error_dict():
    respx.get(f'{BASE}/search/').mock(side_effect=httpx.ConnectError('refused'))
    result = search_servers(query='postgres')
    assert 'error' in result
