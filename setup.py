from setuptools import find_packages, setup

setup(
    name="pypinball",
    version="0.0.1a",
    packages=find_packages(include=["pypinball", "pypinball.*"]),
    package_data={
        "pypinball.resources.audio": ["*.wav"],
        "pypinball.resources.images": ["*.png"],
    },
)
