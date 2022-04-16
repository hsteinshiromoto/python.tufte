import matplotlib.pyplot as plt

from typing import Union
from collections.abc import Iterable
from abc import ABC, abstractmethod
import pandas as pd
from matplotlib.axes import Axes
from pkg_resources import yield_lines
import numpy as np


class Canvas:
    def __init__(
        self,
        plot_type: str,
        x: Iterable[int | float] = None,
        y: Iterable[int | float] = None,
        figsize: tuple = (20, 10),
        ax: Axes = None,
        pad: float = 0.05,
        fontsize: int = 12,
    ):
        self.plot_type = plot_type
        self.x = x
        self.y = y
        self.pad = pad
        self.fontsize = fontsize
        if not ax:
            self.fig, self.ax = plt.subplots(figsize=figsize)

        else:
            self.ax = ax

    def set_spines(
        self,
    ):
        self.ax.tick_params(
            axis="both",
            top="off",
            bottom="off",
            left="off",
            right="off",
            colors="#4B4B4B",
            pad=10,
        )

        self.ax.xaxis.label.set_color("#4B4B4B")
        self.ax.yaxis.label.set_color("#4B4B4B")
        self.ax.spines["top"].set_visible(False)
        self.ax.spines["right"].set_visible(False)

        if self.plot_type.lower() == "bar":
            self.ax.spines["left"].set_visible(False)
            self.ax.spines["bottom"].set_linewidth(0.75)
            self.ax.spines["bottom"].set_edgecolor("LightGray")

        elif self.plot_type.lower() == "box":
            self.ax.spines["left"].set_visible(False)
            self.ax.spines["bottom"].set_visible(False)
            self.ax.tick_params(axis="y", left="on")

        elif self.plot_type.lower() in {"line", "scatter"}:
            self.ax.spines["left"].set_linewidth(0.75)
            self.ax.spines["bottom"].set_linewidth(0.75)
            self.ax.spines["left"].set_edgecolor("#4B4B4B")
            self.ax.spines["bottom"].set_edgecolor("#4B4B4B")

        return None

    @staticmethod
    def fit_axis_range(array: Iterable[int | float], pad: float):

        array_min = array.min().min()
        array_max = array.max().max()
        lower_bound = array_min - ((array_max - array_min) * pad)
        upper_bound = array_max + ((array_max - array_min) * pad)

        return array_min, lower_bound, upper_bound, array_max

    def get_axis_values(
        self,
    ):
        if self.x:
            self.xmin, self.xlower, self.xupper, self.xmax = self.fit_axis_range(
                self.x, self.pad
            )

        if self.y:
            self.ymin, self.ylower, self.yupper, self.ymax = self.fit_axis_range(
                self.y, self.pad
            )

    def set_axis(self, xlim: tuple, xbound: tuple, ylim: tuple, ybound: tuple):

        if self.x:
            self.ax.set_xlim(xmin=min(xlim), xmax=max(xlim))
            self.ax.spines["bottom"].set_bounds(min(xbound), max(xbound))

        if self.y:
            if self.plot_type.lower() == "bar":
                self.ax.set_ylim(ymin=0, ymax=max(ylim))
                self.ax.spines["left"].set_bounds(0, max(ybound))

            else:
                self.ax.set_ylim(min(ylim), max(ylim))
                self.ax.spines["left"].set_bounds(min(ybound), max(ybound))

    def set_ticks(self):

        if self.x:
            xlabels = [
                xl
                for xl in self.ax.xaxis.get_majorticklocs()
                if xl > self.xmin and xl < self.xmax
            ]
            xlabels = [self.xmin] + xlabels + [self.xmax]
            self.ax.set_xticks(xlabels)
            self.ax.set_xticklabels(xlabels, fontsize=self.fontsize)

        if self.y:
            ylabels = [
                yl
                for yl in self.ax.yaxis.get_majorticklocs()
                if yl > self.ymin and yl < self.ymax
            ]
            ylabels = [self.ymin] + ylabels + [self.ymax]
            self.ax.set_yticks(ylabels)
            self.ax.set_yticklabels(ylabels, fontsize=self.fontsize)

    def get_canvas(self) -> Axes:
        self.set_spines()
        self.get_axis_values()
        self.set_axis(
            xlim=(self.xlower, self.xupper),
            xbound=(self.xmin, self.xmax),
            ylim=(self.ylower, self.yupper),
            ybound=(self.ymin, self.ymax),
        )
        self.set_ticks()

        return self.ax


class Plot(ABC, Canvas):
    @abstractmethod
    def plot(self, **kwargs):
        pass

    @staticmethod
    def fit(
        x: Union[str, Iterable],
        y: Union[str, Iterable],
        data: pd.DataFrame = None,
    ):
        x = data[x] if isinstance(x, str) else x
        y = data[y] if isinstance(x, str) else y

        return x, y
