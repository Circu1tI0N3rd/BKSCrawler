'''
crawler.py: Core component of BKSCrawler library

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

#System libraries
import os
import json
import time
import datetime

# 3rd-Party
from html2json import collect as extr
import requests
import nacl.secret as ncs
import nacl.exceptions as nce

# Class required
from .exceptions_errors import *

#Pre-defined context:
# 1 - General Variables
from .predef_vars import *

def OpenSystemy(can, phrase):
    return ncs.SecretBox(phrase).decrypt(can)

#   THE FUNCTION
class StInfoCrawl:
    def __init__(self, username = '', password = '', isEncrypted = False):
        if isEncrypted:
            in_err_res = assert_inerr.format(['username','encrypted password in hex string'])
        else:
            in_err_res = assert_inerr.format(['username','plaintext password string'])
        assert username, in_err_res
        assert password, in_err_res
        self.usr = username
        if isEncrypted:
            try:
                self.pwd = bytes.fromhex(password)
            except ValueError:
                raise AssertionError(in_err_res)
            self.lock = True
        else:
            self.pwd = password
            self.lock = False

        # Define extra variables:
        self.loggedin = False
        self.exptime = 1800

        # Get current week
        today = datetime.datetime.now().date().isocalendar()
        if today[2] == 7:
            # Week end, had to correct the week for this timetable
            self.week = today[1] - 1
        else:
            self.week = today[1]
        del today

    def login(self, phrase = ''):
        # Input check
        if self.lock:
            assert phrase, assert_inerr.format('unlock phrase in hex string')

        # Initialize MyBK session:
        self.ses = requests.Session()

        # Load HCMUT SSO
        try:
            sso = self.ses.get(casLogin)
        except requests.Timeout:
            raise TIMEOUT('SSO GET')
        except requests.ConnectionError:
            raise HTTPErr('CONNECT', 'SSO', e.__dict__)
        except requests.RequestException as e:
            raise HTTPErr('_FORMAT', 'SSO GET', e.__dict__)

        # Getting login session id
        form_key = extr(sso.content, ftk_temp)
        del sso

        # Generating form data
        form = form_sample
        form['username'] = self.usr
        form['lt'] = form_key['LT']
        form['execution'] = form_key['Exec']
        if self.lock:
            try:
                form['password'] = OpenSystemy(self.pwd, bytes.fromhex(phrase)).decode('utf-8')
            except nce.CryptoError as e:
                raise DecryptFail
        else:
            form['password'] = self.pwd

        # Sending POST request
        try:
            cred = self.ses.post(casLogin, data = form, allow_redirects = False)
        except requests.Timeout:
            raise TIMEOUT('SSO POST')
        except requests.ConnectionError:
            raise HTTPErr('CONNECT', 'SSO', e.__dict__)
        except requests.RequestException as e:
            raise HTTPErr('_FORMAT', 'SSO POST', e.__dict__)

        # Error handling for response
        if cred.status_code == 200:
            errors = extr(cred.content, err_temp)
            try:
                assert errors['trace']
            except AssertionError:
                del errors
                pass
            else:
                raise HTTPErr('CAS_200', errors['trace'])
        elif cred.status_code == 302:
            pass
        else:
            raise HTTPErr('HTTP_NO', 'SSO', [cred.status_code, 'login'])

        # Done the cookies, to the portal!
        try:
            st_temp = self.ses.get(cred.headers['Location'])
            # Do another one
            st = self.ses.get(stif['lnk'])
            del st_temp
        except requests.Timeout:
            raise TIMEOUT('MyBK StInfo')
        except requests.ConnectionError:
            raise HTTPErr('CONNECT', 'MyBK StInfo', e.__dict__)
        except requests.RequestException as e:
            raise HTTPErr('_FORMAT', 'MyBK StInfo', e.__dict__)

        # Get STInfo Token
        self.token = extr(st.content, tok_temp)

        # Check if the token exists:
        try:
            assert self.token['_token']
        except AssertionError:
            raise HTTPErr('NOTOKEN')

        # Update the headers
        headers_p = headers_add_template
        headers_p['X-CSRF-TOKEN'] = self.token['_token']
        self.ses.headers.update(headers_p)
        self.loggedin = True
        self.time = time.time()

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
            raise AssertionError(assert_inerr.format(['max_time','unit in min/sec']))
        multiplier = {
            'sec'   :   1,
            'min'   :   60,
        }
        timeout = max_time * multiplier[unit]
        if self.isValidExpire(timeout):
            self.exptime = timeout
        else:
            raise ExpireErr('invd')

    def cleanup(self):
        try:
            del self.ses
            del self.time
            del self.token
        except:
            pass
        self.loggedin = False

    def logout(self, verbose = False):
        '''
        Setting "verbose" to True will throw the exception on logout 
        failure. As most of the exceptions on _request_ is not fully implemented
        (a.k.a. not returning any stacktraces); Therefore, turning this on is
        NOT RECOMMENDED.
        '''
        try:
            out = self.ses.get(casLogout)
        except requests.Timeout:
            # Timeout handling
            self.cleanup()
            if verbose:
                raise TIMEOUT('SSO LOGOUT')
            else:
                pass
        except requests.ConnectionError as e:
            # Connection error handling
            self.cleanup()
            if verbose:
                raise HTTPErr('CONNECT', 'SSO LOGOUT', e.__dict__)
            else:
                pass
        except requests.RequestException as e:
            # Other requests error handling
            self.cleanup()
            if verbose:
                raise HTTPErr('_FORMAT', 'SSO LOGOUT', e.__dict__)
            else:
                pass
        else:
            if out.status_code == 200:
                succ = extr(out.content, succ_temp)
                try:
                    assert succ['trace']
                except AssertionError:
                    self.cleanup()
                    if verbose:
                        raise HTTPErr('_LOGOUT')
                else:
                    del succ
                    del out
                    self.cleanup()
            else:
                self.cleanup()
                if verbose:
                    raise HTTPErr('HTTP_NO', 'SSO', [out.status_code, 'logout (verbose)'])

        # Make sure it actually cleaned and finish gracefully
        self.cleanup()

    def fetch(self, cmd = ''):
        # Check if logged out:
        try:
            assert self.loggedin
        except AssertionError:
            raise ExpireErr('expr')

        # Check if the cookies expired:
        period = int(time.time()-self.time)
        if period > self.exptime:
            self.logout()
            raise ExpireErr('expr')

        # Expiry time validity check:
        if not self.isValidExpire():
            self.logout()
            self.exptime = 1800
            raise ExpireErr('both')

        # Check if cmd is empty
        assert cmd, assert_inerr.format('"cmd" with sched/exam/grade/msg')

        # Check if cmd is valid
        if not cmd in stif['opns']:
            raise AssertionError(assert_inerr.format('"cmd" with sched/exam/grade/msg'))

        # Get the neccessary links to the mem space
        sget = stif['lnk'] + stif['opns'][cmd][0]
        spost = stif['lnk'] + stif['opns'][cmd][1]

        # Get user need
        try:
            pre = self.ses.get(sget)
            table = self.ses.post(spost, json=self.token)
            del pre
            del sget
            del spost
        except requests.Timeout:
            raise TIMEOUT('MyBK StInfo ' + cmd)
        except requests.ConnectionError:
            raise HTTPErr('CONNECT', 'MyBK StInfo ' + cmd, e.__dict__)
        except requests.RequestException as e:
            raise HTTPErr('_FORMAT', 'MyBK StInfo ' + cmd, e.__dict__)

        # Return the JSON
        try:
            return table.json()
        except Exception as e:
            if table.status_code!=200:
                raise HTTPErr('HTTP_NO', 'MyBK StInfo', [table.status_code, 'get ' + cmd])
            else:
                raise RareCrawlerErr('fetch_method_return', e.args)
        del table