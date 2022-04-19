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


class Line(Plot):
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
        _ = self.get_canvas(x, y)

        if linestyle == "tufte":
            # if kwargs:
            warnings.warn("Marker options are being ignored")
            self.ax.plot(
                x,
                y,
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
                x,
                y,
                linestyle=linestyle,
                linewidth=linewidth,
                color=color,
                alpha=alpha,
                markersize=markersize**0.5,
                **kwargs,
            )

        self.set_spines()

        return self.ax

    def set_spines(self):
        self.ax.spines["left"].set_linewidth(0.75)
        self.ax.spines["bottom"].set_linewidth(0.75)
        self.ax.spines["left"].set_edgecolor("#4B4B4B")
        self.ax.spines["bottom"].set_edgecolor("#4B4B4B")

    def set_plot_title(self, title: str = None):
        title = title or f"{Line.__name__} plot of {self.xlabel} and {self.ylabel}"
        super().set_plot_title(title)

    def set_ticks(
        self, xbounds: tuple = None, ybounds: tuple = None, decimals: int = 2, **kwargs
    ):

        if xbounds is not None:
            xmin = min(xbounds)
            xmax = max(xbounds)
            xlabels = [
                np.around(xl, decimals=decimals)
                for xl in self.ax.xaxis.get_majorticklocs()
                if xl > xmin and xl < xmax
            ]
            xlabels = (
                [np.around(xmin, decimals=decimals)]
                + xlabels
                + [np.around(xmax, decimals=decimals)]
            )
            self.ax.set_xticks(xlabels)
            self.ax.set_xticklabels(xlabels, fontsize=self.fontsize)

        if ybounds is not None:
            ymin = min(ybounds)
            ymax = max(ybounds)
            ylabels = [
                np.around(yl, decimals=decimals)
                for yl in self.ax.yaxis.get_majorticklocs()
                if yl > ymin and yl < ymax
            ]
            ylabels = (
                [np.around(ymin, decimals=decimals)]
                + ylabels
                + [np.around(ymax, decimals=decimals)]
            )
            self.ax.set_yticks(ylabels)
            self.ax.set_yticklabels(ylabels, fontsize=self.fontsize)

    def get_axis_values(
        self,
        pad: float,
        x: Iterable[Union[int, float]] = None,
        y: Iterable[Union[int, float]] = None,
    ):
        """Calculates plot limits and axes bounds.

        Args:
            pad (float): Axes bounds padding.
            x (Iterable[int  |  float], optional): x axes iterable. Defaults to None.
            y (Iterable[int  |  float], optional): y axes iterable. Defaults to None.

        Returns:
            _type_: _description_
        """
        axis_values_dict = {}
        if x is not None:
            xmin, xlower, xupper, xmax = self.fit_axis_range(x, pad)
            axis_values_dict["xlim"] = (xlower, xupper)
            axis_values_dict["xbounds"] = (xmin, xmax)

        if y is not None:
            ymin, ylower, yupper, ymax = self.fit_axis_range(y, pad)
            axis_values_dict["ylim"] = (ylower, yupper)
            axis_values_dict["ybounds"] = (ymin, ymax)

        return axis_values_dict


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
