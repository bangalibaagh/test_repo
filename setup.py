"""Setup script for the Device Registry package."""
from setuptools import find_packages, setup

setup(
    name="device-registry",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.100.0",
        "uvicorn[standard]>=0.20.0",
        "sqlalchemy>=2.0.0",
        "pydantic>=2.0.0",
        "pydantic-settings>=2.0.0",
        "httpx>=0.24.0",
    ],
)
