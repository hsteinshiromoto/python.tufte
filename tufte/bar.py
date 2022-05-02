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
        color: str = "gray",
        edgecolor: str = "none",
        width: float = 0.5,
        gridcolor: str = "white",
        **kwargs,
    ):

        x = self.fit(x, data)
        y = self.fit(y, data)
        _ = self.get_canvas({"x": x, "y": y, "pad": 0.05})

        bars = self.ax.bar(
            x, y, align=align, color=color, edgecolor=edgecolor, width=width
        )

        self.ax.bar_label(bars, fmt="%.1f", label_type="edge")

        self.set_bar_spines()

        # xlist = [xl for xl in self.ax.xaxis.get_majorticklocs()]
        # yticklocs = self.ax.yaxis.get_majorticklocs()
        # for y in yticklocs:
        #     self.ax.plot([xlist[0], xlist[-1]], [y, y], color=gridcolor, linewidth=2)

        return self.ax

    def set_bar_spines(self):
        self.ax.spines["left"].set_visible(False)
        self.ax.spines["bottom"].set_visible(False)
        self.ax.axes.get_yaxis().set_visible(False)

    def set_plot_title(self, title: str = None):
        title = title or f"{Bar.__name__} plot of {self.xlabel} and {self.ylabel}"
        super().set_plot_title(title)

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
        **kwargs,
    )
