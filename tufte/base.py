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

    def set_spines(self):
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
        self.ax.xaxis.set_ticks_position("bottom")

        return None

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
        self.set_spines()
        getattr(
            self, f"set_{self.__class__.__name__.lower()}_spines"
        )  # Set specific spines
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
    ) -> np.ndarray:

        try:
            array = data[array]

        except TypeError:
            array = np.array(array)

        return array

    @abstractmethod
    def set_plot_title(self, title: str = None):
        self.ax.set(title=title)
