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


class Box(Plot):
    def plot(
        self,
        array: Union[str, Iterable],
        ticklabelsize: int = 10,
        **kwargs,
    ):
        array = self.fit(array)
        summary_stats = self.get_summary_statistics(array)
        self.ax.plot(
            [0, 0],
            [summary_stats["lower_bound"], summary_stats["25%"]],
            color="black",
            linewidth=0.5,
        )
        self.ax.plot(
            [0, 0],
            [summary_stats["75%"], summary_stats["upper_bound"]],
            color="black",
            linewidth=0.5,
        )
        self.ax.scatter([0], [summary_stats["median"]], color="black", s=5)
        self.ax.axes.get_xaxis().set_visible(False)

        return self.ax

    def set_spines(self):
        pass

    def get_summary_statistics(self, array: Iterable[Union[int, float]]):
        summary_stats = {"min": np.min(array)}
        summary_stats["25%"] = np.percentile(array, 25)
        summary_stats["50%"] = np.median(array)
        summary_stats["75%"] = np.percentile(array, 75)
        summary_stats["max"] = np.max(array)
        summary_stats["mean"] = np.mean(array)
        summary_stats["std"] = np.std(array)
        summary_stats["iqr"] = summary_stats["75%"] - summary_stats["25%"]
        summary_stats["lower_bound"] = summary_stats["25%"] - 1.5 * summary_stats["iqr"]
        summary_stats["upper_bound"] = summary_stats["75%"] + 1.5 * summary_stats["iqr"]

        return summary_stats

    def set_plot_title(self, title: str = None):
        title = title or f"{Line.__name__} plot of {self.xlabel} and {self.ylabel}"
        super().set_plot_title(title)

    def set_ticks(
        self, xbounds: tuple = None, ybounds: tuple = None, decimals: int = 2
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
        x=x,
        y=y,
        data=data,
        xlabel=xlabel,
        ylabel=ylabel,
        figsize=figsize,
        fontsize=fontsize,
        ax=ax,
    )
    line.set_plot_title(title)

    return line.plot(
        linestyle=linestyle,
        linewidth=linewidth,
        color=color,
        alpha=alpha,
        ticklabelsize=ticklabelsize,
        markersize=markersize,
        **kwargs,
    )
