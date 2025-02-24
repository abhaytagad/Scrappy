# Automatically created by: shub deploy

from setuptools import setup, find_packages

setup(
    name         = 'project',
    version      = '1.0',
    packages     = find_packages(),
    entry_points = {'scrapy': ['settings = hindi_scraper.settings']},
    install_requires=[
        'Scrapy',
        'scrapy_monkeylearn==0.2.5',
        'langdetect'
        # Add other dependencies here
    ],
)
