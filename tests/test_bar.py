import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.testing.decorators import image_comparison, check_figures_equal

PROJECT_ROOT = Path.cwd().resolve().parent
sys.path.append(str(PROJECT_ROOT))

from tufte.bar import main as barplot

REFERENCE_FILENAME = "reference_bar.eps"


def make_reference_figure():
    x = ["A", "B", "C", "D", "E", "F"]
    y = np.array([41, 23, 48, 84, 32, 38])

    ax = barplot(x, y.flatten())

    plt.savefig(REFERENCE_FILENAME)

    return ax


def get_figure(filename: Path):
    with open(str(filename), "r") as f:
        figure = f.read()

    return figure


@check_figures_equal()
def test_plot(fig_test, fig_ref):
    fig_test.subplots().plot([1, 3, 5])
    fig_ref.subplots().plot([0, 1, 2], [1, 3, 5])


@image_comparison(
    baseline_images=["make_reference_figure"], remove_text=True, extensions=["png"]
)
def test_line_dashes():
    ax = make_reference_figure()


def test_figure():
    make_reference_figure()
    x = ["A", "B", "C", "D", "E", "F"]
    y = np.array([41, 23, 48, 84, 32, 38])

    ax = barplot(x, y.flatten())
    plt.savefig("test_bar.eps")

    reference_figure = get_figure(REFERENCE_FILENAME)
    test_figure = get_figure("test_bar.eps")

    assert test_figure == reference_figure
