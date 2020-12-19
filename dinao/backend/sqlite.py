"""Implementation of SQLite backends."""
import sqlite3
from urllib.parse import parse_qs, urlparse

from dinao.backend.base import Connection, ConnectionPool


class ConnectionSQLite3(Connection):
    """Implementation of Connection for Sqlite3."""

    def _execute(self, cursor, sql: str, params: tuple = None):
        if params:
            return cursor.execute(sql, params)
        cursor.execute(sql)


class ConnectionPoolSQLite3(ConnectionPool):
    """Implementation of ConnectionPool for SQLite3."""

    def __init__(self, db_url: str):
        """Construct a connection pool for the given connection URL.

        The db_url is expected to be in the following format::

            "sqlite3://{filename}"

        Obviously, this is not a real "pool", all connections given out by lease will be new connections.

        :param db_url: a url with the described format
        :raises: ConfigurationError, BackendEngineNotInstalled
        """
        super().__init__(db_url)
        self._cnx_kwargs = self._url_to_cnx_kwargs(db_url)

    def _url_to_cnx_kwargs(self, url: str):
        db_url = urlparse(url)
        additional_args = parse_qs(db_url.query)
        self._raise_for_unexpected_ars([], additional_args)
        return {"database": db_url.path}

    def lease(self) -> Connection:  # noqa: D102
        inner_cnx = sqlite3.connect(**self._cnx_kwargs)
        return ConnectionSQLite3(inner_cnx)

    def release(self, cnx: Connection):  # noqa: D102
        cnx._cnx.close()

    @property
    def mung_symbol(self) -> str:  # noqa: D102
        return "?"