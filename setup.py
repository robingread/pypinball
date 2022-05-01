from setuptools import setup, find_packages

setup(
    name="pypinball",
    version="0.0.1a",
    packages=find_packages(include=['pypinball', 'pypinball.*']),
    package_data={"pypinball.resources.audio": ["*.wav"]},
)
