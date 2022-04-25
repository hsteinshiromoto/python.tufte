import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).resolve().parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="tufte",
    version="0.1.0",
    description="A Tufte-inspired style for plotting data.",
    long_description_content_type="text/markdown",
    long_description=README,
    url="https://github.com/hsteinshiromoto/tufte",
    author="Humberto STEIN SHIROMOTO",
    author_email="h.stein.shiromoto@gmail.com",
    # license="GPL",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["tufte"],
    include_package_data=True,
    install_requires=["pandas", "numpy", "matplotlib", "typeguard", "deprecated"],
    entry_points={
        "console_scripts": [
            "tufte=tufte.__main__:main",
        ]
    },
)
