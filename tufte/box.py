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
        self.ax.scatter([0], [summary_stats["50%"]], color="black", s=5)
        self.ax.axes.get_xaxis().set_visible(False)
        self.get_canvas({"array": array, "pad": 0.05})

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
        title = title or f"{Box.__name__} plot of {self.xlabel} and {self.ylabel}"
        super().set_plot_title(title)

    def get_axis_values(
        self,
        pad: float,
        array: Iterable[Union[int, float]] = None,
    ):
        """Calculates plot limits and axes bounds.

        Args:
            pad (float): Axes bounds padding.
            x (Iterable[int  |  float], optional): x axes iterable. Defaults to None.
            y (Iterable[int  |  float], optional): y axes iterable. Defaults to None.

        Returns:
            _type_: _description_
        """

        min_val, lower, upper, max_val = self.fit_axis_range(array, pad)
        return {"xlim": (lower, upper), "xbounds": (min_val, max_val)}

    def set_ticks(self, xbounds: tuple, **kwargs):
        min_val = min(xbounds)
        max_val = max(xbounds)
        range_val = max_val - min_val
        self.ax.set_ylim(min_val - range_val * 0.05, max_val + range_val * 0.05)


def main(
    array: Union[str, Iterable],
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
    box = Box(
        xlabel=xlabel,
        ylabel=ylabel,
        figsize=figsize,
        fontsize=fontsize,
        ax=ax,
    )
    box.set_plot_title(title)

    return box.plot(
        array=array,
        data=data,
        linestyle=linestyle,
        linewidth=linewidth,
        color=color,
        alpha=alpha,
        ticklabelsize=ticklabelsize,
        markersize=markersize,
        **kwargs,
    )
