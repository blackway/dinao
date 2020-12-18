"""Miscellaneous tests for backend utilities."""

from dinao.backend import create_connection_pool
from dinao.backend.errors import ConfigurationError, UnsupportedBackend

import pytest


@pytest.mark.parametrize(
    "db_uri, match, except_class",
    [
        ("://user:pass@host:4444", "No database backend specified", ConfigurationError),
        ("oracle://user:pass@host:4444", "not supported", UnsupportedBackend),
        ("postgresql+psycopg3://user:pass@host:4444", "not supported", UnsupportedBackend),
        ("postgresql://user:pass@host:4444", "name is required but missing", ConfigurationError),
        ("postgresql://user:pass@host:4444/dbname?pool_max_conn=ABC", "must be integer", ConfigurationError),
        ("postgresql://user:pass@host:4444/dbname?pool_min_conn=ABC", "must be integer", ConfigurationError),
        (
            "postgresql://user:pass@host:4444/dbname?pool_min_conn=1&pool_min_conn=2",
            "single value",
            ConfigurationError,
        ),
    ],
)
def test_backend_create_rejection(db_uri: str, match: str, except_class):
    """Tests bad db_url are rejected by create_connection_pool."""
    with pytest.raises(except_class, match=match):
        create_connection_pool(db_uri)
