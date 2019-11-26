'''
THIS IS LOCALE-RELATED VARIABLES CONTAINER
'''
locale = 'en'


# Error senarios template
errtypes = {
        'SUCCESS'   :   'The operation completed successfully',
        'CAS_200'   :   'The HCMUT SSO returned and error.',
        'CASHTTP'   :   'The HCMUT SSO responded weirdly',
        'TIMEOUT'   :   'A timeout occurred; Possible connection interruption/misconfigured.',
        'CONNERR'   :   'Error while connecting to host; interruption concerned',
        'HTTPERR'   :   'Error occurred while establishing connection. Check the connection and retry; If the problem persists, please file an issue on GitHub.',
        'EXP_ERR'   :   'Invalid maximum expiration time (must be no more than 30 mins)',
        'EXPIRED'   :   'The MyBK session has expired. Please do the login again',
        'ERR_INP'   :   'Recieved no/invalid value(s) when expected. Check "stack" object for what is/are missing/needed',
        'NCD_ERR'   :   'Error while decrypting password, check if the phrase and/or encrypted password is/are correct, otherwise supply it again or recreate those'
}

# Function usage table
uasge = {
	'init' : {
		'usage': 'StInfoCrawl(<username>, <encrypted_password>, [locale (optional)])',
		'username': 'Your HCMUT username',
		'encrypted_password': 'Your password encrypted with NaCl SecretBox in hex form',
		'locale': 'The desired language you want your error descriptions to be in (does not count )'
	}
}