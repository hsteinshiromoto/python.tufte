import sys
import tempfile
from collections.abc import Iterable
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pytest
from matplotlib.axes import Axes
from PIL import Image

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from tufte.bar import main as barplot

REFERENCE_IMAGE = "reference_bar.png"
REFERENCE_PATH = PROJECT_ROOT / "tests" / "images"


def make_figure(x: Iterable, y: Iterable, path: Path, filename: str) -> Axes:
    ax = barplot(x, y)

    plt.savefig(str(path / filename))

    return ax


def make_reference_figure() -> Path:
    x = ["A", "B", "C", "D", "E", "F"]
    y = np.array([41, 23, 48, 84, 32, 38]).flatten()

    make_figure(x, y, REFERENCE_PATH, REFERENCE_IMAGE)


def make_test_figure(
    x: Iterable = ["A", "B", "C", "D", "E", "F"],
    y: Iterable = np.array([41, 23, 48, 84, 32, 38]).flatten(),
    path: Path = Path(tempfile.mkdtemp()),
    filename: str = "test_image.png",
) -> Path:

    make_figure(x, y, path, filename)

    return path / filename


@pytest.fixture(params=[["A", "B", "C", "D", "E", "F"], ["A", "B", "C", "D", "E", "F"]])
def parse_test_figure(request):
    return request.param


def test_images_equal(parse_test_figure):
    """_summary_

    Args:
        image_1 (str, optional): _description_. Defaults to REFERENCE_FILENAME.
        image_2 (str, optional): _description_. Defaults to "test_bar.png".

    References:
        [1] https://www.redshiftzero.com/pytest-image/

    """
    reference_image = Image.open(str(REFERENCE_PATH / REFERENCE_IMAGE))
    path = make_test_figure(x=parse_test_figure)
    img2 = Image.open(path)

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


if __name__ == "__main__":
    path = make_reference_figure()
    print(path)
