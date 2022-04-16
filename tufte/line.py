import matplotlib.pyplot as plt

from typing import Union
from collections.abc import Iterable
import pandas as pd
import warnings

from base import Plot, Canvas
from matplotlib.axes import Axes


class Line(Plot):
    def __init__(
        self,
        figsize: tuple = (20, 10),
        ax: Axes = None,
        fontsize: int = 12,
    ):

        Canvas.__init__(
            self,
            plot_type=Line.__name__,
            figsize=figsize,
            ax=ax,
            fontsize=fontsize,
        )

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
        **kwargs
    ):
        x, y = self.fit(x, y, data)

        if linestyle == "tufte":
            if kwargs:
                warnings.warn("Marker options are being ignored")
                self.ax.plot(
                    self.x,
                    self.y,
                    linestyle="-",
                    linewidth=linewidth,
                    color=color,
                    alpha=alpha,
                    zorder=1,
                )
                self.ax.scatter(
                    x, y, marker="o", s=markersize * 8, color="white", zorder=2  # type: ignore
                )
                self.ax.scatter(x, y, marker="o", s=markersize, color=color, zorder=3)  # type: ignore

        else:
            self.ax.plot(
                self.x,
                self.y,
                linestyle=linestyle,
                linewidth=linewidth,
                color=color,
                alpha=alpha,
                markersize=markersize**0.5,
                **kwargs
            )

        return self.fig, self.ax

    def set_spines(self):
        self.ax.spines["left"].set_linewidth(0.75)
        self.ax.spines["bottom"].set_linewidth(0.75)
        self.ax.spines["left"].set_edgecolor("#4B4B4B")
        self.ax.spines["bottom"].set_edgecolor("#4B4B4B")
