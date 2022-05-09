import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.testing.decorators import image_comparison, check_figures_equal
from PIL import Image

PROJECT_ROOT = Path.cwd().resolve().parent
sys.path.append(str(PROJECT_ROOT))

from tufte.bar import main as barplot

REFERENCE_FILENAME = "reference_bar.png"


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
    plt.savefig("test_bar.png")

    reference_figure = get_figure(REFERENCE_FILENAME)
    test_figure = get_figure("test_bar.png")

    assert test_figure == reference_figure


def test_images_equal(image_1: str = REFERENCE_FILENAME, image_2: str = "test_bar.png"):
    """_summary_

    Args:
        image_1 (str, optional): _description_. Defaults to REFERENCE_FILENAME.
        image_2 (str, optional): _description_. Defaults to "test_bar.png".

    References:
        [1] https://www.redshiftzero.com/pytest-image/

    """
    img1 = Image.open(image_1)
    img2 = Image.open(image_2)

    # Convert to same mode and size for comparison
    img2 = img2.convert(img1.mode)
    img2 = img2.resize(img1.size)

    sum_sq_diff = np.sum(
        (np.asarray(img1).astype("float") - np.asarray(img2).astype("float")) ** 2
    )

    if sum_sq_diff == 0:
        # Images are exactly the same
        assert True
    else:
        normalized_sum_sq_diff = sum_sq_diff / np.sqrt(sum_sq_diff)
        assert normalized_sum_sq_diff < 0.001
