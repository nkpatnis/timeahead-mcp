try:
    from importlib.metadata import version
    __version__ = version('timeahead-mcp')
except Exception:
    __version__ = '0.1.0'
