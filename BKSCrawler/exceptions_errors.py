'''
EXCEPTIONS AND ERRORS DEFINITION FILE FOR CRAWLER
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