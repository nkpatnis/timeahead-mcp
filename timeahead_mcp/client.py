"""
HTTP client for the timeahead backend.

Reads two env vars:
  TIMEAHEAD_BASE_URL  — defaults to https://timeahead.in
  TIMEAHEAD_API_KEY   — optional; unlocks higher rate limits
  TIMEAHEAD_TIMEOUT   — seconds, defaults to 15

All functions return the parsed JSON body on success.
On network or HTTP errors they return a dict with an "error" key so
the AI assistant receives a clean message instead of an unhandled exception.
"""

import os

import httpx

from timeahead_mcp import __version__

_BASE_URL = os.environ.get('TIMEAHEAD_BASE_URL', 'https://timeahead.in').rstrip('/')
_API_KEY  = os.environ.get('TIMEAHEAD_API_KEY', '')
_TIMEOUT  = float(os.environ.get('TIMEAHEAD_TIMEOUT', '15'))


def _headers() -> dict:
    h = {
        'Accept': 'application/json',
        'User-Agent': f'timeahead-mcp/{__version__}',
    }
    if _API_KEY:
        h['X-API-Key'] = _API_KEY
    return h


def get(path: str, params: dict | None = None) -> dict | list:
    url = f'{_BASE_URL}/mcp/v1/{path.lstrip("/")}'
    try:
        r = httpx.get(url, params=params, headers=_headers(), timeout=_TIMEOUT)
        r.raise_for_status()
        return r.json()
    except httpx.HTTPStatusError as e:
        return {
            'error': f'API error {e.response.status_code}: {e.response.text[:200]}',
            'status_code': e.response.status_code,
        }
    except httpx.RequestError as e:
        return {'error': f'Could not reach timeahead.in: {e}. Check your network connection.'}
