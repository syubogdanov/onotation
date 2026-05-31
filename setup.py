from setuptools import setup
from build import build

setup_kwargs = {
    "name": "onotation",
}

build(setup_kwargs)

setup(**setup_kwargs)