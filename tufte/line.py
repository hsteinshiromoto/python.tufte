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
        x: Union[str, Iterable],
        y: Union[str, Iterable],
        data: pd.DataFrame = None,
        figsize: tuple = (20, 10),
        ax: Axes = None,
        pad: float = 0.05,
        fontsize: int = 12,
    ):
        x, y = self.fit(x, y, data)
        Canvas.__init__(
            self,
            x=x,
            y=y,
            plot_type=Line.__name__,
            figsize=figsize,
            ax=ax,
            pad=pad,
            fontsize=fontsize,
        )

    @staticmethod
    def fit(
        x: Union[str, Iterable],
        y: Union[str, Iterable],
        data: pd.DataFrame = None,
    ):
        x = data[x] if isinstance(x, str) else x
        y = data[y] if isinstance(x, str) else y

        return x, y

    def plot(
        self,
        linestyle: str = "tufte",
        linewidth: float = 1.0,
        color: str = "black",
        alpha: float = 0.9,
        ticklabelsize: int = 10,
        markersize: int = 10,
        **kwargs
    ):

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
