'''
exceptions_error.py: Exceptions and errors definition file of BKSCrawler library

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

# EXCEPTIONS
#Vars
expr_types = {
	'invd':	'Invalid maximum expiration time (must be no more than 30 mins)',
	'expr': 'MyBK session expired',
	'both':	'Invalid max expiration time and session expired'
}
http_err_types = {
	'CAS_200':	'The HCMUT SSO Service responded with "{0}"',
	'HTTP_NO':	'The HCMUT {0} Service returned HTTP code {1[0]} while {1[1]}',
	'CONNECT':	'Error connecting to HCMUT {0} Service; From requests: {1}',
	'_FORMAT':	'Formating error at {0}; requests said: {1}',
	'NOTOKEN':	'The HCMUT MyBK StInfo Service failed to respond',
	'_LOGOUT':	'The HCMUT SSO Service logout without any notifications'
}
#Vars for Python-handled exceptions
assert_inerr = 'Input(s) blank/invalid, expected valid {0}'	#For AssertionError Exception
#Classes
class CrawlerError(Exception):
    def __init__(self, args, nil=None):
        self.args = args
        self.Reduced = nil
        super(CrawlerError, self).__init__(args)

class TIMEOUT(CrawlerError):
	def __init__(self, where):
		super().__init__('Request timed out while at {0}'.format(where))

class ExpireErr(CrawlerError):
	def __init__(self, what):
		super().__init__(expr_types[what])

class HTTPErr(CrawlerError):
	def __init__(self, what, where='', how=''):
		super().__init__(http_err_types[what].format(where, how))

class DecryptFail(CrawlerError):
	def __init__(self):
		super().__init__('Failed decrypting encrypted password from phrase')

class RareCrawlerErr(CrawlerError):
	def __init__(self, where, data_pls):
		super().__init__('Please report this error with how to reproduce it. Source: {0}; Stacktrace: {1}'.format(where, data_pls))

# ERRORS
# Pre-configured answer
errtypes = {
        'SUCCESS'   :   'The operation completed successfully'
}