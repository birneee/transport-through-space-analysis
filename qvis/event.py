from typing import Optional


class Event:
    inner: dict
    connection: 'connection.Connection'

    def __init__(self, inner: dict, connection: 'connection.Connection'):
        self.inner = inner
        self.connection = connection

    @property
    def index(self) -> int:
        """unique index of the event"""
        return getattr(self.inner, 'Index')

    @property
    def time(self) -> float:
        """in seconds"""
        return self.inner['time']

    @property
    def name(self) -> str:
        """name of the event"""
        return self.inner['name']

    @property
    def data(self) -> Optional[dict]:
        """event specific data"""
        return self.inner.get('data')
