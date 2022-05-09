import sys
import warnings
from pathlib import Path
from typing import Iterable, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.axes import Axes

PROJECT_ROOT = Path.cwd().resolve().parent
sys.path.append(str(PROJECT_ROOT))

from tufte.line import Line
from tufte.bar import Bar
from tufte.base import Plot


class LineBar(Plot):
    """
    Implements Plot class for line plot.

    Args:
        Plot: Plot class

    Example:
        >>> n_samples = 5
        >>> x = range(n_samples)
        >>> y = np.random.rand(n_samples, 1)
        >>> linebar = LineBar(xlabel="xlabel", ylabel="ylabel")
        >>> print(linebar)
        LineBar(xlabel='xlabel', ylabel='ylabel', ax=<AxesSubplot:>, fontsize=18, figsize=(20, 10))
    """

    def plot(
        self,
        x: Union[str, Iterable],
        yline: Union[str, Iterable],
        ybar: Union[str, Iterable],
        ax_line: Axes,
        ax_bar: Axes,
        data: pd.DataFrame = None,
        **kwargs,
    ):
        pass

    def set_plot_title(self, title: str = None):
        title = title or f"{LineBar.__name__} plot of {self.xlabel} and {self.ylabel}"
        super().set_plot_title(title)


def main(
    x: str | Iterable,
    yline: str | Iterable,
    ybar: str | Iterable,
    data: pd.DataFrame = None,
    xlabel: str = "x",
    yline_label: str = "yline",
    ybar_label: str = "ybar",
    title: str = None,
    figsize: tuple = (20, 10),
    fontsize: int = 12,
    ax_line: Axes = None,
    ax_bar: Axes = None,
    sharex: bool = False,
    **kwargs,
):

    if (ax_line is None) | (ax_bar is None):
        fig, (ax_line, ax_bar) = plt.subplots(nrows=2, figsize=figsize, sharex=sharex)

    line = Line(
        xlabel=xlabel,
        ylabel=yline_label,
        figsize=figsize,
        fontsize=fontsize,
        ax=ax_line,
    )
    line.set_plot_title(title)

    ax_line = line.plot(
        x=x,
        y=yline,
        data=data,
        **kwargs,
    )

    bar = Bar(
        xlabel=xlabel,
        ylabel=ybar_label,
        figsize=figsize,
        fontsize=fontsize,
        ax=ax_line,
    )
    bar.set_plot_title(title)

    ax_bar = bar.plot(
        x=x,
        y=ybar,
        data=data,
        **kwargs,
    )

    return ax_line, ax_bar
