from setuptools import find_packages, setup

setup(
    name="mma-stats",
    packages=find_packages(exclude=["mma-stats_tests"]),
    install_requires=[
        "dagster==1.7.*",
        "pandas",
        "beautifulsoup4==4.12.3"

    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
