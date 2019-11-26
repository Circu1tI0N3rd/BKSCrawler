'''
VARIABLES STORAGE NOTICE:
This file is only used for storing variables neccessary for the main class.
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
