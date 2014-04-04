# -*- coding: utf-8 -*-
#
# 2014 Alex Silva <alexsilvaf28 at gmail.com>

"""
Usage:
    python setup.py install
"""

from setuptools import setup#, find_packages

setup(
	name="Playfulbot",
	description="Playfulbet auto-bet",
	version="1.1.2",
	author="Alex Silva",
	author_email="h4ll0ck at gmail dot com",
	url="https://github.com/Alexsays/Playfulbot",
	license="GNU General Public License (GPLv2)",
	packages = ["command_line", ],
	entry_points = {
        'console_scripts': [
            'playfulbot = command_line.playfulbot:main'
        ]
    },
	install_requires=[
		"mechanize",
		"beautifulsoup4",
		"colorama"
	]
)
