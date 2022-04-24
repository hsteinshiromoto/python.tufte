from abc import ABC, abstractmethod
from collections.abc import Generator, Iterable
from dataclasses import dataclass
from re import X
from typing import Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.axes import Axes
from pkg_resources import yield_lines

params = {  #'figure.dpi' : 200,
    "figure.facecolor": "white",
    "axes.axisbelow": True,
    "lines.antialiased": True,
    "savefig.facecolor": "white",
}

for (k, v) in params.items():
    plt.rcParams[k] = v


@dataclass
class Canvas(ABC):
    """Defines the figure container

    Args:
        figsize (tuple): Size of canvas.
        fontsize (int): Font size.
        xlabel (str): Name of x axis.
        ylabel (str): Name of y axis.
        ax (Axes, optional): Matplotlib axes. Defaults to None.
    """

    xlabel: str
    ylabel: str
    ax: Axes = None
    fontsize: int = 18
    figsize: tuple = (20, 10)

    def __post_init__(self):
        if self.ax is None:
            self.fig, self.ax = plt.subplots(figsize=self.figsize)

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
        self.ax.spines["top"].set_visible(False)
        self.ax.spines["right"].set_visible(False)

        # Ensure that the axis ticks only show up on the bottom and left of the plot.
        self.ax.get_xaxis().tick_bottom()
        self.ax.get_yaxis().tick_left()

        """Remove this commented code

        elif self.plot_type.lower() == "box":
            self.ax.spines["left"].set_visible(False)
            self.ax.spines["bottom"].set_visible(False)
            self.ax.tick_params(axis="y", left="on")


        """

        return None

    def set_axis(
        self,
        xlim: tuple = None,
        xbounds: tuple = None,
        ylim: tuple = None,
        ybounds: tuple = None,
    ):
        """Defines axes limits and spines lengths

        Args:
            xlim (tuple, optional): Max and min values of x spine. Defaults to None.
            xbound (tuple, optional): Max and min values of x limits. Defaults to None.
            ylim (tuple, optional): Max and min values of y spine. Defaults to None.
            ybound (tuple, optional): Max and min values of y limits. Defaults to None.
        """

        if (xlim is not None) & (xbounds is not None):
            self.ax.set_xlim(xmin=min(xlim), xmax=max(xlim))
            self.ax.spines["bottom"].set_bounds(min(xbounds), max(xbounds))

        if (ylim is not None) & (ybounds is not None):
            self.ax.set_ylim(min(ylim), max(ylim))
            self.ax.spines["left"].set_bounds(min(ybounds), max(ybounds))

    @abstractmethod
    def set_ticks(self, **kwargs):
        pass

    @staticmethod
    def fit_axis_range(array: np.array, pad: float):
        """Calculates spine and limits of a given array to be ploted

        Args:
            array (np.array): Array to be plotted.
            pad (float): Additional padding to the limits.

        Returns:
            float: Bounds of spine and limits of the plot.
        """

        array_min = array.min().min()
        array_max = array.max().max()
        lower_bound = array_min - ((array_max - array_min) * pad)
        upper_bound = array_max + ((array_max - array_min) * pad)

        return array_min, lower_bound, upper_bound, array_max

    @abstractmethod
    def get_axis_values(self, **kwargs) -> dict:
        pass

    @abstractmethod
    def set_spines(self, **kwargs):
        """Set canvas spines"""
        pass

    def set_axes_labels(self):
        self.ax.set(xlabel=f"{self.xlabel}", ylabel=f"{self.ylabel}")

    def get_canvas(self, kwargs) -> Axes:
        """Format figure container

        Args:
            x (Iterable[int  |  float]): x axes.
            y (Iterable[int  |  float]): y axes.
            pad (float, optional): Axes bounds padding. Defaults to 0.05.

        Returns:
            Axes: Figure container
        """
        self.set_base_spines()
        self.set_spines()
        axis_values_dict = self.get_axis_values(**kwargs)
        self.set_axis(**axis_values_dict)
        self.set_ticks(**axis_values_dict)
        self.set_axes_labels()

        return self.ax


class Plot(Canvas):
    """
    Defines the plot content

    Args:
        Canvas (Canvas): Figure container
    """

    xlabel: str
    ylabel: str
    ax: Axes = None
    fontsize: int = 18
    figsize: tuple = (20, 10)

    @abstractmethod
    def plot(self, **kwargs):
        pass

    @staticmethod
    def fit(
        array: Union[str, Generator, Iterable],
        data: pd.DataFrame = None,
    ) -> np.array:

        try:
            array = data[array]

        except TypeError:
            array = np.array(array)

        return array

    @abstractmethod
    def set_plot_title(self, title: str = None):
        self.ax.set(title=title)
