import sys
from pathlib import Path
from collections.abc import Iterable

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.testing.decorators import image_comparison, check_figures_equal
from PIL import Image
import pytest
import tempfile
from matplotlib.axes import Axes

PROJECT_ROOT = Path.cwd().resolve().parent
sys.path.append(str(PROJECT_ROOT))

from tufte.bar import main as barplot

REFERENCE_IMAGE = "reference_bar.png"


def make_figure(x: Iterable, y: Iterable) -> Axes:
    return barplot(x, y)


@pytest.fixture(scope="module")
def make_reference_figure(filename: str = REFERENCE_IMAGE) -> Path:
    x = ["A", "B", "C", "D", "E", "F"]
    y = np.array([41, 23, 48, 84, 32, 38]).flatten()

    ax = make_figure(x, y)

    path = Path(tempfile.mkdtemp())

    plt.savefig(str(path / filename))

    return path


@pytest.fixture
def call_reference_figure(request):
    make_reference_figure(request.param)


@pytest.mark.parametrize("call_reference_figure", [REFERENCE_IMAGE, "test_bar.png"])
def test_images_equal(call_reference_figure):
    """_summary_

    Args:
        image_1 (str, optional): _description_. Defaults to REFERENCE_FILENAME.
        image_2 (str, optional): _description_. Defaults to "test_bar.png".

    References:
        [1] https://www.redshiftzero.com/pytest-image/

    """
    reference_image = Image.open(REFERENCE_IMAGE)
    img2 = Image.open("test_bar.png")

    # Convert to same mode and size for comparison
    img2 = img2.convert(reference_image.mode)
    img2 = img2.resize(reference_image.size)

    sum_sq_diff = np.sum(
        (np.asarray(reference_image).astype("float") - np.asarray(img2).astype("float"))
        ** 2
    )

    if sum_sq_diff != 0:
        normalized_sum_sq_diff = sum_sq_diff / np.sqrt(sum_sq_diff)
        assert normalized_sum_sq_diff < 0.001
