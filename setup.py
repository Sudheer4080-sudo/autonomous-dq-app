
from setuptools import setup, find_packages

setup(
    name="autonomous-dq-agent",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "pyyaml",
        "streamlit"
    ],
)
