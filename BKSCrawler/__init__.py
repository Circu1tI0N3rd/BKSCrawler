'''
BKSCrawler library initializer

This library provides the ease of use to get information from
HCMUT Student Information Portal.

Copyright (C) 2019  Maurice Klivoslov

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

# Main class
from .crawler import StInfoCrawl
# Exception class
from .exceptions_errors import CrawlerError, TIMEOUT, ExpireErr, HTTPErr, DecryptFail, RareCrawlerErr