from abc import ABC, abstractmethod
from collections.abc import Iterable
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


class Canvas(ABC):
    def __init__(
        self,
        figsize: tuple,
        fontsize: int,
        xlabel: str,
        ylabel: str,
        ax: Axes = None,
    ):
        """Defines the figure container

        Args:
            figsize (tuple): Size of canvas.
            fontsize (int): Font size.
            xlabel (str): Name of x axis.
            ylabel (str): Name of y axis.
            ax (Axes, optional): Matplotlib axes. Defaults to None.

        Returns:
            _type_: _description_
        """
        self.fontsize = fontsize
        self.xlabel = xlabel
        self.ylabel = ylabel
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
            #! TODO: Fix this case
            #  if self.plot_type.lower() == "bar":
            #     self.ax.set_ylim(ymin=0, ymax=max(ylim))
            #     self.ax.spines["left"].set_bounds(0, max(ybound))

            # else:
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

    @abstractmethod
    def set_spines(self, **kwargs):
        """Set canvas spines"""
        pass

    def set_axes_labels(self):
        self.ax.set(xlabel=f"{self.xlabel}", ylabel=f"{self.ylabel}")

    def get_canvas(
        self,
        x: Iterable[Union[int, float]],
        y: Iterable[Union[int, float]],
        pad: float = 0.05,
    ) -> Axes:
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
        axis_values_dict = self.get_axis_values(pad, x, y)
        self.set_axis(**axis_values_dict)
        self.set_ticks(
            xbounds=axis_values_dict["xbounds"], ybounds=axis_values_dict["ybounds"]
        )
        self.set_axes_labels()

        return self.ax


class Plot(Canvas):
    def __init__(
        self,
        xlabel: str,
        ylabel: str,
        figsize: tuple = (20, 10),
        ax: Axes = None,
        fontsize: int = 18,
    ):
        super().__init__(
            xlabel=xlabel, ylabel=ylabel, figsize=figsize, fontsize=fontsize, ax=ax
        )
        self.set_plot_title()

    @abstractmethod
    def plot(self, **kwargs):
        pass

    @staticmethod
    def fit(
        x: Union[str, Iterable],
        y: Union[str, Iterable],
        data: pd.DataFrame = None,
    ) -> np.array:
        x = data[x] if isinstance(x, str) else np.array(x)
        y = data[y] if isinstance(x, str) else np.array(y)

        return x, y

    @abstractmethod
    def set_plot_title(self, title: str = None):
        self.ax.set(title=title)
