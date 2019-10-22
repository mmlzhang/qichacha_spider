# Automatically created by: scrapyd-deploy

from . import __version__

from setuptools import setup, find_packages

project_name = "bigcrawler"

setup(
    name=project_name,
    version=__version__,
    packages=find_packages(),
    entry_points={'scrapy': ['settings = crawler.settings']},
)
