from typing import OrderedDict

from matplotlib.axes import Axes
from matplotlib.patches import StepPatch
from matplotlib.ticker import FuncFormatter
import numpy as np

from connection import Connection

def byte_axis_formatter(bytes: int, position: int) -> str:
    if bytes > 1000000:
        return f'{bytes/1000000:.0f}M'
    if bytes > 1000:
        return f'{bytes/1000:.0f}K'
    return f'{bytes:.0f}'

QvisTimeAxisFormatter = FuncFormatter(lambda seconds, position: f'{seconds:.0f}')
QvisByteAxisFormatter = FuncFormatter(byte_axis_formatter)

def plot_connection_flow_limit(ax: Axes, conn: Connection) -> StepPatch:
    seconds, limits = zip(*conn.connection_flow_limit_updates())
    seconds = list(seconds)
    seconds.insert(0, 0)
    return ax.stairs(values=limits, edges=seconds, baseline=None, color='#a80f3a', label='Connection flow control limit')


def plot_data_sent(ax: Axes, conn: Connection):
    times, length = zip(*map(lambda f: (f.time(), f.length()),
        filter(lambda f: f.type() == 'stream', 
            conn.sentFrames())))
    cum_length = np.cumsum(length)
    ax.scatter(x=times, y=cum_length, s=2, rasterized=True, label='Data sent (includes retransmits)', color='#0000ff')