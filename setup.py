import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="s4s",
    version="1.0.2",
    description="Service for Script",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Priezt/s4s",
    author="Priezt",
    license="MIT",
    packages=["s4s"],
    include_package_data=True,
    install_requires=["flask"],
    entry_points={
        "console_scripts": [
            "s4s=s4s.__main__:main",
        ]
    },
)
