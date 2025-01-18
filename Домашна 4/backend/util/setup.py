from setuptools import setup, find_packages

setup(
    name="preprocess",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["pandas", "numpy"],
    description="Shared utilities for preprocessing data",
    author="Daniel Ilievski",
    license="MIT",
)