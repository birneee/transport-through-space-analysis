from collections import namedtuple
from typing import Iterator, Optional

import pandas as pd

from frame import Frame


class Packet:
    inner: namedtuple

    def __init__(self, inner: pd.Series):
        self.inner = inner

    def time(self) -> float:
        """in seconds"""
        return getattr(self.inner, 'time')

    def frames(self) -> Iterator['Frame']:
        data = getattr(self.inner, 'data')
        if data is None:
            return
        frames = data.get('frames')
        if frames is None:
            return
        for frame in frames:
            yield Frame(frame, self)