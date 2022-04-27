from gettext import ngettext
import sys
import warnings
from pathlib import Path
from typing import Iterable, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.axes import Axes

PROJECT_ROOT = Path.cwd().resolve().parent
sys.path.append(str(PROJECT_ROOT))

from tufte.base import Plot


class Bar(Plot):
    # TODO: redo this class!
    def plot(
        self,
        x: str | Iterable,
        y: str | Iterable,
        data: pd.DataFrame = None,
        align: str = "center",
        color: str = "LightGray",
        edgecolor: str = "none",
        width: float = 0.5,
        gridcolor: str = "white",
        **kwargs,
    ):

        x = self.fit(x, data)
        y = self.fit(y, data)
        _ = self.get_canvas({"x": x, "y": y, "pad": 0.05})

        self.ax.bar(x, y, align=align, color=color, edgecolor=edgecolor, width=width)

        axis_values_dict = self.fit_axis_values(x, y)
        self.set_ticks(axis_values_dict["x"]["range"], align, width, gridcolor)
        self.set_axis(xlim=(0, 0), xbounds=(0, 0), ylim=(0, 0), ybounds=(0, 0))

        return self.ax

    def set_Bar_spines(self):
        self.ax.spines["left"].set_visible(False)
        self.ax.spines["bottom"].set_linewidth(0.75)
        self.ax.spines["bottom"].set_edgecolor("LightGray")

    def set_plot_title(self, title: str = None):
        title = title or f"{Bar.__name__} plot of {self.xlabel} and {self.ylabel}"
        super().set_plot_title(title)

    def set_ticks(
        self,
        xrange: Iterable[int | float],
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

        xmin = min(xrange)
        xmax = max(xrange)

        xlist = [
            xl for xl in self.ax.xaxis.get_majorticklocs() if xl >= xmin and xl <= xmax
        ]
        xlist = [xmin - lower_buffer] + xlist[1:-1] + [xmax + upper_buffer]
        yticklocs = self.ax.yaxis.get_majorticklocs()
        for y in yticklocs:
            self.ax.plot([xlist[0], xlist[-1]], [y, y], color=gridcolor, linewidth=1.25)

    def fit_axis_values(
        self,
        x: Iterable[int | float | str],
        y: Iterable[int | float | str],
    ):
        """Calculates plot limits and axes bounds.

        Args:
            x (Iterable[int  |  float | str]): x axes iterable.
            y (Iterable[int  |  float | str]): y axes iterable.

        Returns:
            _type_: _description_
        """
        xvalues = np.unique(x) if isinstance(next(x), str) else x
        yvalues = np.unique(y) if isinstance(next(y), str) else y

        return {
            "x": {"range": range(len(xvalues))},
            "y": {"range": range(len(yvalues))},
        }

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
    bar = Bar(
        xlabel=xlabel,
        ylabel=ylabel,
        figsize=figsize,
        fontsize=fontsize,
        ax=ax,
    )
    bar.set_plot_title(title)

    return bar.plot(
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
