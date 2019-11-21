#System libraries
import os
import json

# 3rd-Party
from html2json import collect as extr
import requests

#Pre-defined context:
# 1 - Extraction template
ftk_temp = {
    'url'   :   ['#fm1', 'action', []],
    'LT'    :   ['input[name=lt]', 'value', []],
    'Exec'  :   ['input[name=execution]', 'value', []]
}
err_temp = {
    'code'  :   ['.errors', None, []]
}
tok_temp = {
    '_token':  ['meta[name=_token]', 'content', []]
}
# 2 - Links
CASURL = 'https://sso.hcmut.edu.vn'
ReqSubURL = '/cas/login?service=http://mybk.hcmut.edu.vn/stinfo/'
LogoutURL = '/cas/logout?service=http://mybk.hcmut.edu.vn/stinfo/'
STIURL = 'https://mybk.hcmut.edu.vn/stinfo'
PREAJURL = '/lichhoc'
AJURL = '/lichthi/ajax_lichhoc'

#   THE FUNCTION
def get_timetable(username = '', password = ''):
        # A bit of example
        if username == '' and password == '':
            return {
                'usage' :   'get_timetable(<username>, <password>)',
                'return':   'JSON Object'
            }
        
        # Generate new cookie request session
        s = requests.Session()
        try:
            sso = s.get(CASURL + ReqSubURL)

            # Getting login session id
            form_key = extr(sso.content, ftk_temp)

            # Generating form data
            form = {
                'username'  :   username,
                'password'  :   password,
                'lt'        :   form_key['LT'],
                'execution' :   form_key['Exec'],
                '_eventId'  :   'submit',
                'submit'    :   'Login'
            }
            del sso

            # Sending POST request
            cred = s.post(CASURL + form_key['url'], data = form, allow_redirects = False)
            if cred.status_code != 302:
                errors = extr(cred.content, err_temp)
                errors['http'] = cred.status_code
                return errors
                del cred

            # Successfully requested
            st1 = s.get(cred.headers['Location'])
            st2 = s.get(STIURL)

            # Get STInfo Token
            token = extr(st2.content, tok_temp)

            # Update the headers
            headers_p = {
                'X-CSRF-TOKEN'  :   token['_token'],
                'X-Requested-With'  :   'XMLHttpRequest'
            }
            s.headers.update(headers_p)
            del st1
            del st2
            del cred

            # Get schedule
            pre = s.get(STIURL + PREAJURL)
            table = s.post(STIURL + AJURL, json=token)
            del pre

            # Now end the session
            logout = s.get(CASURL + LogoutURL, allow_redirects = False)
            del logout

            # Return the schedule
            timetable = table.json()
            del table
            return {
                'http'  :   0,
                'code'  :   timetable
            }
        except Exception as e:
            return {
                'http'  :   666,
                'code'  :   str(e)
            }