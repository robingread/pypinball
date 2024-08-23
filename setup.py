from setuptools import find_packages, setup

setup(
    name="pypinball",
    version="0.0.1a",
    packages=find_packages(include=["pypinball", "pypinball.*"]),
    package_data={
        "pypinball.resources.audio": ["*.mp3", "*.wav"],
        "pypinball.resources.images": ["*.png"],
    },
    entry_points={"console_scripts": ["pypinball = pypinball.main:main"]},
)
