#System libraries
import os
import json
import time

# 3rd-Party
from html2json import collect as extr
import requests
import nacl.secret as ncs
import nacl.exceptions as nce

# Class required
from .exceptions import *

#Pre-defined context:
# 1 - General Variables
from .predef_vars import *

# 2 - Error template
errtypes = {
        'SUCCESS'   :   'The operation completed successfully',
        'CAS_200'   :   'The HCMUT SSO returned and error, please check "stack" object for more details',
        'CASHTTP'   :   'The HCMUT SSO responded weirdly, check "stack" object for details; Less likely possible server error',
        'TIMEOUT'   :   'A timeout occurred; Possible connection interruption/misconfigured.',
        'CONNERR'   :   'Error while connecting to host; interruption concerned',
        'HTTPERR'   :   'Error occurred while establishing connection. Check the connection and retry; If the problem persists, please file an issue along with content of "stack" object.',
        'EXP_ERR'   :   'Invalid maximum expiration time (must be no more than 30 mins)',
        'EXPIRED'   :   'The MyBK session has expired. Please do the login again',
        'ERR_INP'   :   'Recieved no/invalid value(s) when expected. Check "stack" object for what is/are missing/needed',
        'NCD_ERR'   :   'Error while decrypting password, check if the phrase and/or encrypted password is/are correct, otherwise supply it again or recreate those'
}

def GenRes(errtype, *stack):
    resp = dict()
    resp['code'] = errtype
    try:
        resp['desc'] = errtypes[errtype]
    except:
        resp['desc'] = 'Please find in "stack" object'
    if stack:
        if len(stack) > 1:
            resp['stack'] = [component for component in stack]
        else:
            resp['stack'] = stack[0]
    return resp

def OpenSystemy(can, phrase):
    return ncs.SecretBox(phrase).decrypt(can)

#   THE FUNCTION
class StInfoCrawl:
    def __init__(self, username = '', password = '', isEncrypted = False):
        if username == '' and password == '':
            raise CrawlerError(GenRes('ERR_INP', {'expected': ['username', 'password']}))
        else:
            self.usr = username
            if isEncrypted:
                self.pwd = bytes.fromhex(password)
                self.lock = True
            else:
                self.pwd = password
                self.lock = False

        # Define extra variables:
        self.loggedin = False
        self.exptime = 1800

    def login(self, phrase = ''):
        # Input check
        if self.lock and phrase == '':
            return GenRes('ERR_INP', {'expected': 'phrase_in_hex_string'})

        # Initialize MyBK session:
        self.ses = requests.Session()

        # Load HCMUT SSO
        try:
            sso = self.ses.get(casLogin)
        except requests.Timeout as e:
            # Timeout handling
            return GenRes('TIMEOUT', e.__dict__)
        except requests.ConnectionError as e:
            # Connection error handling
            return GenRes('CONNERR', e.__dict__)
        except requests.RequestException as e:
            # Other requests error handling
            raise CrawlerError(GenRes('HTTPERR', {'where': 'CAS_GET'}, e.__dict__))

        # Getting login session id
        form_key = extr(sso.content, ftk_temp)
        del sso

        # Generating form data
        if self.lock:
            try:
                form = {
                    'username'  :   self.usr,
                    'password'  :   OpenSystemy(self.pwd, bytes.fromhex(phrase)).decode('utf-8'),
                    'lt'        :   form_key['LT'],
                    'execution' :   form_key['Exec'],
                    '_eventId'  :   'submit',
                    'submit'    :   'Login'
                }
            except nce.CryptoError as e:
                return GenRes('NCD_ERR', e.args)
        else:
            form = {
                'username'  :   self.usr,
                'password'  :   self.pwd,
                'lt'        :   form_key['LT'],
                'execution' :   form_key['Exec'],
                '_eventId'  :   'submit',
                'submit'    :   'Login'
            }

        # Sending POST request
        try:
            cred = self.ses.post(casLogin, data = form, allow_redirects = False)
        except requests.Timeout as e:
            # Timeout handling
            return GenRes('TIMEOUT', e.__dict__)
        except requests.ConnectionError as e:
            # Connection error handling
            return GenRes('CONNERR', e.__dict__)
        except requests.RequestException as e:
            # Other requests error handling
            raise CrawlerError(GenRes('HTTPERR', {'where': 'CAS_POST'}, e.__dict__))

        # Error handling for response
        if cred.status_code == 200:
            errors = extr(cred.content, err_temp)
            if errors['trace'] != None:
                errors['http'] = cred.status_code
                del cred
                return GenRes('CAS_200', errors)
            else:
                del errors
        elif cred.status_code == 302:
            pass
        else:
            raise CrawlerError(GenRes('CASHTTP', {
                    'http': cred.status_code,
                    'trace': cred.reason
                }))
            del cred

        # Done the cookies, to the portal!
        try:
            st_temp = self.ses.get(cred.headers['Location'])
            # Do another one
            st = self.ses.get(stif['lnk'])
            del st_temp
        except requests.Timeout as e:
            # Timeout handling
            return GenRes('TIMEOUT', e.__dict__)
        except requests.ConnectionError as e:
            # Connection error handling
            return GenRes('CONNERR', e.__dict__)
        except requests.RequestException as e:
            # Other requests error handling
            raise CrawlerError(GenRes('HTTPERR', {'where': 'CAS_POST'}, e.__dict__))

        # Get STInfo Token
        self.token = extr(st.content, tok_temp)

        # Check if the token exists:
        if self.token['_token'] == None:
            self.logout()
            raise CrawlerError('NO TOKEN!')

        # Update the headers
        headers_p = {
            'X-CSRF-TOKEN'  :   self.token['_token'],
            'X-Requested-With'  :   'XMLHttpRequest'
        }
        self.ses.headers.update(headers_p)
        self.loggedin = True
        self.time = time.time()
        # Set time here
        return GenRes('SUCCESS')

    def isValidExpire(self, *value):
        if value:
            if value[0] > 1800:
                return False
            else:
                return True
        else:
            if self.exptime > 1800:
                return False
            else:
                return True

    def setExpire(self, max_time = 30, unit = 'min'):
        if not unit in ('sec', 'min'):
            raise CrawlerError(GenRes('EXP_ERR'))
        multiplier = {
            'sec'   :   1,
            'min'   :   60,
        }
        timeout = max_time * multiplier[unit]
        if self.isValidExpire(timeout):
            self.exptime = timeout
        else:
            raise CrawlerError(GenRes('EXP_ERR'))

    def cleanup(self):
        try:
            del self.ses
            del self.time
            del self.token
        except:
            pass

    def logout(self, verbose = False):
        '''
        Setting "verbose" to True will throw the exception on logout 
        failure. As most of the exceptions on _request_ is not fully implemented
        (a.k.a. not returning any stacktraces); Therefore, turning this on is
        NOT RECOMMENDED.
        '''
        try:
            out = self.ses.get(casLogout)
        except requests.Timeout as e:
            # Timeout handling
            self.cleanup()
            if verbose:
                return GenRes('TIMEOUT', e.__dict__)
            else:
                pass
        except requests.ConnectionError as e:
            # Connection error handling
            self.cleanup()
            if verbose:
                return GenRes('CONNERR', e.__dict__)
            else:
                pass
        except requests.RequestException as e:
            # Other requests error handling
            self.cleanup()
            if verbose:
                return GenRes('HTTPERR', {'where': 'CAS_LOGOUT_VONLY'}, e.__dict__)
            else:
                pass
        else:
            succ = extr(out.content, succ_temp)
            if succ['trace'] == None:
                self.cleanup()
                if verbose:
                    return GenRes('LOGOUT_FAILED', 'Server not returned any success identification, or I have not implemented it yet.')
            else:
                del succ
                del out
                self.cleanup()

        # Make sure it actually cleaned and finish gracefully
        try:
            del self.time
            del self.ses
        except:
            pass
        return GenRes('SUCCESS')

    def fetch(self, cmd = ''):
        # Check if cmd is empty
        if cmd == '':
            raise CrawlerError(GenRes('ERR_INP', {'expected': ['sched','exam','grade','msg']}))

        # Get the neccessary links to the mem space
        try:
            sget = stif['lnk'] + stif['opns'][cmd][0]
            spost = stif['lnk'] + stif['opns'][cmd][1]
        except:
            # cmd is invalid
            raise CrawlerError(GenRes('ERR_INP', {'expected': ['sched','exam','grade','msg']}))

        # Expiry time validity check:
        if not self.isValidExpire():
            temp = logout()
            del temp
            raise CrawlerError(GenRes('EXPIRED'))

        # Check if the cookies expired:
        period = int(time.time()-self.time)
        if period > self.exptime:
            temp = logout()
            del temp
            raise CrawlerError(GenRes('EXPIRED'))

        # No error found, get user need
        try:
            pre = self.ses.get(sget)
            table = self.ses.post(spost, json=self.token)
            del pre
            del sget
            del spost
        except requests.Timeout as e:
            # Timeout handling
            return GenRes('TIMEOUT', e.__dict__)
        except requests.ConnectionError as e:
            # Connection error handling
            return GenRes('CONNERR', e.__dict__)
        except requests.RequestException as e:
            # Other requests error handling
            raise CrawlerError(GenRes('HTTPERR', {'where': 'CAS_POST'}, e.__dict__))

        # Return the JSON
        try:
            return table.json()
        except Exception as e:
            # If cannot return the dict, throw an error
            raise CrawlerError(GenRes('HTTPERR', e.args))
        del table