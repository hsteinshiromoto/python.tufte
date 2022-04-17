from abc import ABC, abstractmethod
from collections.abc import Iterable
from re import X
from typing import Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.axes import Axes
from pkg_resources import yield_lines


class Canvas(ABC):
    """Defines the figure container"""

    def __init__(
        self,
        figsize: tuple,
        fontsize: int,
        ax: Axes = None,
    ):
        self.fontsize = fontsize
        self.plot_type = plot_type
        if not ax:
            self.fig, self.ax = plt.subplots(figsize=figsize)

        else:
            self.ax = ax

    def set_base_spines(self):
        """Set figure spines"""
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

        """Remove this commented code

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
        """

        return None

    def set_axis(
        self,
        xlim: tuple = None,
        xbound: tuple = None,
        ylim: tuple = None,
        ybound: tuple = None,
    ):
        """Defines axes limits and spines lengths

        Args:
            xlim (tuple, optional): Max and min values of x spine. Defaults to None.
            xbound (tuple, optional): Max and min values of x limits. Defaults to None.
            ylim (tuple, optional): Max and min values of y spine. Defaults to None.
            ybound (tuple, optional): Max and min values of y limits. Defaults to None.
        """

        if bool(xlim) & bool(xbound):
            self.ax.set_xlim(xmin=min(xlim), xmax=max(xlim))
            self.ax.spines["bottom"].set_bounds(min(xbound), max(xbound))

        if bool(ylim) & bool(ybound):
            if self.plot_type.lower() == "bar":
                self.ax.set_ylim(ymin=0, ymax=max(ylim))
                self.ax.spines["left"].set_bounds(0, max(ybound))

            else:
                self.ax.set_ylim(min(ylim), max(ylim))
                self.ax.spines["left"].set_bounds(min(ybound), max(ybound))

    def set_ticks(self, xbounds: tuple = None, ybounds: tuple = None):

        if xbounds:
            xmin = min(xbounds)
            xmax = max(xbounds)
            xlabels = [
                xl
                for xl in self.ax.xaxis.get_majorticklocs()
                if xl > xmin and xl < xmax
            ]
            xlabels = [xmin] + xlabels + [xmax]
            self.ax.set_xticks(xlabels)
            self.ax.set_xticklabels(xlabels, fontsize=self.fontsize)

        if ybounds:
            ymin = min(ybounds)
            ymax = max(ybounds)
            ylabels = [
                yl
                for yl in self.ax.yaxis.get_majorticklocs()
                if yl > ymin and yl < ymax
            ]
            ylabels = [ymin] + ylabels + [ymax]
            self.ax.set_yticks(ylabels)
            self.ax.set_yticklabels(ylabels, fontsize=self.fontsize)

    @staticmethod
    def fit_axis_range(array: Iterable[int | float], pad: float):
        """Calculates spine and limits of a given array to be ploted

        Args:
            array (Iterable[int  |  float]): Array to be plotted.
            pad (float): Additional padding to the limits.

        Returns:
            float: Bounds of spine and limits of the plot.
        """

        array_min = array.min().min()
        array_max = array.max().max()
        lower_bound = array_min - ((array_max - array_min) * pad)
        upper_bound = array_max + ((array_max - array_min) * pad)

        return array_min, lower_bound, upper_bound, array_max

    def get_axis_values(
        self, x: Iterable[int | float], y: Iterable[int | float], pad: float
    ):
        axis_values_dict = {}
        if x:
            xmin, xlower, xupper, xmax = self.fit_axis_range(x, pad)
            axis_values_dict["xlim"] = (xlower, xupper)
            axis_values_dict["xbound"] = (xmin, xmax)

        if y:
            ymin, ylower, yupper, ymax = self.fit_axis_range(y, pad)
            axis_values_dict["ylim"] = (ylower, yupper)
            axis_values_dict["ybound"] = (ymin, ymax)

        return axis_values_dict

    @abstractmethod
    def set_spines(self):
        pass

    def get_canvas(
        self, x: Iterable[int | float], y: Iterable[int | float], pad: float = 0.05
    ) -> Axes:
        self.set_base_spines()
        self.set_spines()
        axis_values_dict = self.get_axis_values(x, y, pad)
        self.set_axis(**axis_values_dict)
        self.set_ticks(
            xbounds=axis_values_dict["xbounds"], ybounds=axis_values_dict["ybounds"]
        )

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
