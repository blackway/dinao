"""Functionality abstracting the primitive database backend interface."""

from urllib.parse import urlparse

from dinao.backend.base import Connection, ConnectionPool, ResultSet
from dinao.backend.errors import ConfigurationError, UnsupportedBackend
from dinao.backend.postgres import ConnectionPoolPSQLPsycopg2


ENGINE_DEFAULTS = {"postgresql": "psycopg2"}


def create_connection_pool(db_url: str) -> ConnectionPool:
    """Create a connection pool for the given database connection URL.

    The db_url is expected to be in the following format::

        "{db_backend}+{driver}://{username}:{password}@{hostname}:{port}/{db_name}"

    With different db_backends / drivers supporting additional arguments.

    :return: A connection pool based on the given database URL.
    :raises: ConfigurationError, UnsupportedBackend
    """
    parsed_url = urlparse(db_url)
    backend = parsed_url.scheme
    if not backend:
        raise ConfigurationError("No database backend specified")
    backend = backend.split("+")
    engine = ENGINE_DEFAULTS.get(backend[0]) if len(backend) == 1 else backend[1]
    backend = backend[0]
    if backend == "postgresql" and engine == "psycopg2":
        return ConnectionPoolPSQLPsycopg2(db_url)
    raise UnsupportedBackend(f'The backend+engine "{parsed_url.scheme}" is not supported')


__all__ = ["Connection", "ConnectionPool", "ResultSet", "create_connection_pool", "errors"]
