from gettext import ngettext
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


class Bar(Plot):
    def plot(
        self,
        x: Union[str, Iterable],
        y: Union[str, Iterable],
        data: pd.DataFrame = None,
        align: str = "center",
        color: str = "LightGray",
        edgecolor: str = "none",
        width: float = 0.5,
        gridcolor: str = "white",
        **kwargs,
    ):
        x, y = self.fit(x, y, data)

        self.ax.bar(x, y, align=align, color=color, edgecolor=edgecolor, width=width)

        return self.ax

    def set_spines(self):
        self.ax.spines["left"].set_visible(False)
        self.ax.spines["bottom"].set_linewidth(0.75)
        self.ax.spines["bottom"].set_edgecolor("LightGray")

    def set_plot_title(self, title: str = None):
        title = title or f"{Line.__name__} plot of {self.xlabel} and {self.ylabel}"
        super().set_plot_title(title)

    def get_canvas(
        self,
        x: Iterable[Union[int, float]],
        y: Iterable[Union[int, float]],
        align: str,
        width: float,
        gridcolor: str,
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
        xvalues, yvalues = self.get_axis_values(x, y)
        axis_values_dict["ylim"] = (0, max(axis_values_dict["ylim"]))

        axis_values_dict["xlim"] = self.set_ticks(
            align, width, axis_values_dict["xbounds"], gridcolor
        )
        self.set_axis(**axis_values_dict)
        self.set_axes_labels()

        return self.ax

    def set_ticks(
        self,
        xvalues: Iterable[int | float],
        yvalues: Iterable[int | float],
        align: str,
        width: float,
        gridcolor: str,
    ):
        if align.lower() == "center":
            lower_buffer = 0.5
            upper_buffer = 0.5

        elif align.lower() == "edge":
            lower_buffer = 0.25
            upper_buffer = width + 0.25

        else:
            msg = f"Expected align to be either center of edge. Got {align}."
            raise ValueError(msg)

        xmin = min(xvalues)
        xmax = max(xvalues)

        xlist = [
            xl for xl in self.ax.xaxis.get_majorticklocs() if xl >= xmin and xl <= xmax
        ]
        xlist = [xmin - lower_buffer] + xlist[1:-1] + [xmax + upper_buffer]
        yticklocs = self.ax.yaxis.get_majorticklocs()
        for y in yticklocs:
            self.ax.plot([xlist[0], xlist[-1]], [y, y], color=gridcolor, linewidth=1.25)

    def get_axis_values(
        self,
        x: Iterable[Union[int, float, str]],
        y: Iterable[Union[int, float, str]],
    ):
        """Calculates plot limits and axes bounds.

        Args:
            x (Iterable[int  |  float | str]): x axes iterable.
            y (Iterable[int  |  float | str]): y axes iterable.

        Returns:
            _type_: _description_
        """
        xvalues = np.unique(x)
        yvalues = np.unique(y)

        return xvalues, yvalues

    def auto_rotate_xticklabel(self):
        figw = self.fig.get_figwidth()
        nticks = len(self.ax.xaxis.get_majorticklocs())
        tick_spacing = figw / float(nticks)
        font_size = [v.get_fontsize() for v in self.ax.xaxis.get_majorticklabels()][0]
        FONT_RATE = 0.01
        char_width = font_size * FONT_RATE
        max_labelwidth = (
            max(len(v.get_text()) for v in self.ax.xaxis.get_majorticklabels())
            * char_width
        )

        if float(max_labelwidth) / tick_spacing >= 0.90:
            plt.xticks(rotation=90)


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
    line = Bar(
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
