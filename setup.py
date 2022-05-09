import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

print(README)

# This call to setup() does all the work
setup(
    name="tufte",
    version="0.2.3",
    description="A Tufte-inspired style for plotting data",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/hsteinshiromoto/tufte",
    author="Humberto STEIN SHIROMOTO",
    author_email="h.stein.shiromoto@gmail.com",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: ``Python :: 3.10",
    ],
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    install_requires=["pandas", "numpy", "matplotlib", "typeguard", "deprecated"],
)
