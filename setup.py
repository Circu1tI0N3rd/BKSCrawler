from setuptools import setup, find_packages
setup(name = 'BKSCrawler',
	version = 0.1,
	url = 'https://github.com/Circu1tI0N3rd/BKSCrawler',
	license = 'GPLv3',
	author = 'Maurice Klivoslov',
	author_email = 'brainstormingeveryday@gmail.com',
	description = 'A Python library that crawls JSON-formatted timetable from HCMUT StInfo Portal',
	packages = find_packages(exclude=['tests']),
	long_description = open('README.md').read(),
	zip_safe = False)