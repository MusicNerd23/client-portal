"""Test package initializer.

Expose a placeholder `client` so statements like `from . import client`
in test modules succeed. The actual Flask test client is provided by the
pytest fixture defined in `tests/conftest.py`, and the fixture injection
via the test function parameter named `client` takes precedence.
"""

client = None
