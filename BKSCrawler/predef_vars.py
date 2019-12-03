'''
predef_vars.py: Default varialbles definition file component of BKSCrawler library

This library provides the ease of use to get information from
HCMUT Student Information Portal.

VARIABLES STORAGE NOTICE:
This file is only used for storing variables neccessary for the main class.

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

# Variables
#CAS
casLogin = 'https://sso.hcmut.edu.vn/cas/login?service=http://mybk.hcmut.edu.vn/stinfo/'
casLogout = 'https://sso.hcmut.edu.vn/cas/logout'
#MyBK StInfo
stif = {
    'lnk'   :   'https://mybk.hcmut.edu.vn/stinfo',
    'opns'  :   {
        'sched' :   ['/lichhoc', '/lichthi/ajax_lichhoc'],
        'exam'  :   ['/lichthi', '/lichthi/ajax_lichthi'],
        'grade' :   ['/grade', '/grade/ajax_grade'],
        'msg'   :   ['/message', '/message/data']
    }
}

# Some extraction templates
ftk_temp = {
    'url'   :   ['#fm1', 'action', []],
    'LT'    :   ['input[name=lt]', 'value', []],
    'Exec'  :   ['input[name=execution]', 'value', []]
}
err_temp = {
    'trace'  :   ['.errors', None, []]
}
succ_temp = {
    'trace'  :   ['.success', None, []]
}
tok_temp = {
    '_token':  ['meta[name=_token]', 'content', []]
}
# Requests templates
form_sample = {
    'username'  :   '',
    'password'  :   '',
    'lt'        :   '',
    'execution' :   '',
    '_eventId'  :   'submit',
    'submit'    :   'Login'
}
headers_add_template = {
    'X-CSRF-TOKEN'  :   '',
    'X-Requested-With'  :   'XMLHttpRequest'
}