from setuptools import setup, find_packages

setup(
    name="pentago_game",
    version="0.0.1",
    packages=find_packages(),
    install_requires=["gymnasium", "numpy", "pettingzoo", "pygame"],
)