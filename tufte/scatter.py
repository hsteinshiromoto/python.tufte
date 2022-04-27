import sys
import warnings
from pathlib import Path
from typing import Iterable, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.axes import Axes

ROOT_PATH = Path.cwd().resolve().parent
SOURCE_PATH = ROOT_PATH / "tufte"
sys.path.append(str(SOURCE_PATH))

from base import Plot


class Scatter(Plot):
    """
    Implements Plot class for line plot.

    Args:
        Plot: Plot class.

    Example:
        >>> n_samples = 5
        >>> x = range(n_samples)
        >>> y = np.random.rand(n_samples, 1)
        >>> scatter = Scatter(xlabel="xlabel", ylabel="ylabel")
        >>> print(line)
        Scatter(xlabel='xlabel', ylabel='ylabel', ax=<AxesSubplot:>, fontsize=18, figsize=(20, 10))
    """

    def plot(
        self,
        x: Union[str, Iterable],
        y: Union[str, Iterable],
        data: pd.DataFrame = None,
        linestyle: str = "tufte",
        linewidth: float = 1.0,
        color: str = "black",
        alpha: float = 0.9,
        ticklabelsize: int = 10,
        markersize: int = 10,
        **kwargs,
    ):
        x = self.fit(x, data)
        y = self.fit(y, data)
        _ = self.get_canvas({"x": x, "y": y, "pad": 0.05})

        if linestyle == "tufte":
            # if kwargs:
            warnings.warn("Marker options are being ignored")
            self.ax.scatter(
                x,
                y,
                marker="o",
                s=markersize,
                linewidth=linewidth,
                color=color,
                alpha=alpha,
                zorder=1,
            )

        return self.ax

    def set_Scatter_spines(self):
        self.ax.spines["left"].set_linewidth(0.75)
        self.ax.spines["bottom"].set_linewidth(0.75)
        self.ax.spines["left"].set_edgecolor("#4B4B4B")
        self.ax.spines["bottom"].set_edgecolor("#4B4B4B")

    def set_plot_title(self, title: str = None):
        title = title or f"{Scatter.__name__} plot of {self.xlabel} and {self.ylabel}"
        super().set_plot_title(title)


def main(
    x: Union[str, Iterable],
    y: Union[str, Iterable],
    data: pd.DataFrame = None,
    xlabel: str = "x",
    ylabel: str = "y",
    title: str = None,
    linestyle: str = "tufte",
    linewidth: float = 1.0,
    color: str = "black",
    alpha: float = 0.9,
    ticklabelsize: int = 10,
    markersize: int = 10,
    figsize: tuple = (20, 10),
    fontsize: int = 12,
    ax: Axes = None,
    **kwargs,
):
    scatter = Scatter(
        xlabel=xlabel,
        ylabel=ylabel,
        figsize=figsize,
        fontsize=fontsize,
        ax=ax,
    )
    scatter.set_plot_title(title)

    return scatter.plot(
        x=x,
        y=y,
        data=data,
        linestyle=linestyle,
        linewidth=linewidth,
        color=color,
        alpha=alpha,
        ticklabelsize=ticklabelsize,
        markersize=markersize,
        **kwargs,
    )
