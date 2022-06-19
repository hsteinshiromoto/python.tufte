import sys
import warnings
from pathlib import Path
from typing import Iterable, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.axes import Axes

PROJECT_ROOT = Path.cwd().resolve().parent
sys.path.append(str(PROJECT_ROOT))

from tufte.base import Plot


class Line(Plot):
    """
    Implements Plot class for line plot.

    Args:
        Plot: Plot class

    Example:
        >>> n_samples = 5
        >>> x = range(n_samples)
        >>> y = np.random.rand(n_samples, 1)
        >>> line = Line(xlabel="xlabel", ylabel="ylabel")
        >>> print(line)
        Line(xlabel='xlabel', ylabel='ylabel', ax=<AxesSubplot:>, fontsize=18, figsize=(20, 10))
    """

    def plot(
        self,
        x: str | Iterable | None = None,
        y: str | Iterable | None = None,
        hue: str | Iterable | None = None,
        data: pd.DataFrame | None = None,
        hue_order: Iterable | None = None,
        estimator: str = "mean",
        ci: int = 95,
        linewidth: float = 2.0,
        color: str = "black",
        alpha: float = 0.9,
        ticklabelsize: int = 10,
        markersize: int = 10,
        **kwargs,
    ):
        x = self.fit(x, data)
        y = (self.fit(y, data),)
        _ = self.get_canvas({"x": x, "y": y, "pad": 0.05})

        self.ax = sns.lineplot(
            x=x,
            y=y,
            hue=hue,
            data=data,
            hue_order=hue_order,
            estimator=estimator,
            ci=ci,
            ax=self.ax,
            **{"linewidth": linewidth, "alpha": alpha},
        )

        self.ax = sns.scatterplot(
            x=x,
            y=y,
            data=data,
            hue=hue,
            marker="o",
            estimator=estimator,
            ci=ci,
            size=markersize * 8,
            color="white",
            ax=self.ax,
            **{"zorder": 2},  # type: ignore
        )

        self.ax = sns.scatterplot(
            x=x,
            y=y,
            data=data,
            hue=hue,
            marker="o",
            estimator=estimator,
            ci=ci,
            ax=self.ax,
            **{"zorder": 3},  # type: ignore
        )

        return self.ax

    def set_line_spines(self):
        self.ax.spines["left"].set_linewidth(0.75)
        self.ax.spines["bottom"].set_linewidth(0.75)
        self.ax.spines["left"].set_edgecolor("#4B4B4B")
        self.ax.spines["bottom"].set_edgecolor("#4B4B4B")

        # Ensure that the axis ticks only show up on the bottom and left of the plot.
        self.ax.get_xaxis().tick_bottom()
        self.ax.get_yaxis().tick_left()

    def set_plot_title(self, title: str = None):
        title = title or f"{Line.__name__} plot of {self.xlabel} and {self.ylabel}"
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
    line = Line(
        xlabel=xlabel,
        ylabel=ylabel,
        figsize=figsize,
        fontsize=fontsize,
        ax=ax,
    )
    line.set_plot_title(title)

    return line.plot(
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
