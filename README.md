
# BKSCrawler

## What is this?
 This is a Python library I wrote based on the following 2 sources:
  - Packet capturing from Wireshark,
  - And _PythonTryHard_'s [BKSchedule_Rewrite](https://github.com/PythonTryHard/BKSchedule_Rewrite)

The library uses **3** additional libraries: [_html2json_](http://pypi.org/project/html2json/), [_requests_](https://pypi.org/project/requests/) and [_pyNaCl_](http://pypi.org/project/pynacl) (all in Python).

When supplied with _a username_, _an encrypted password_ and _an encryption phrase (pyNaCl)_, the library produces a JSON-formatted output which can be either:
- The schedule;
- The exam timetable;
- Announcements;
- Or the grading as your preferences

The credential information above must be able to access [HCMUT MyBK Portal](https://mybk.hcmut.edu.vn).
 
## Main aims
- Fixes some issues with the original BKSchedule_Rewrite above;
- Adding a logout method;
- Letting others the possiblity to propagates the tables for their tastes.

## Usage
Assuming you are in Python 3.7 shell and already install all requirements:

	python3 pip install requests html2json pynacl

### Usage:
- Initalize:

    >>> import BKSCrawler as bk
    >>> mybk = bk.StInfoCrawl(<Your username here>, <Your NaCl-encrypted password here>)
    >>> mybk.login(<Your NaCl encryption phrase here>)
    [A JSON OUTPUT]

- Get your information (say, timetable) from HCMUT StInfo Portal:

    >>> mybk.fetch('sched')
    [A JSON OUTPUT]

_Valid commands are:_
- 'sched': Get timetable;
- 'grade': Get exam gradings;
- 'exam': Get exam schedule;
- 'msg': Get annoucements available.

- Log out of the portal:

    >>> mybk.logout()
    [A 'SUCCESS' JSON RESPONSE]

- Change expiry time of the session:

    >>> mybk.setExpire(<time_in_int>, <Format: min|sec>)
    [NO OUTPUT]

***NOTE:*** The maximum allowed period is ***30 minutes***

## Exceptions
The function will throw `BKSCrawler.CrawlerError` during the crawling process for the following commands:
- On initialization of the session: Missing inputs;
- `login`: For specific errors that needs attention;
- `setExpire`: Invalid period;
- `fetch`: Any errors.

***_Format:_*** _JSON_(at _`BKSCrawler.CrawlerError.args`_)

    {
      'code'  : <Error_code>,
      'desc'  : <Brief_details_about_the_error>,
      'trace' : <Detailed_output>
    }

Whereas the error can be:
- 'CAS_200'   :   'The HCMUT SSO returned and error, please check "stack" object for more details',
- 'CASHTTP'   :   'The HCMUT SSO responded weirdly, check "stack" object for details; Less likely possible server error',
- 'TIMEOUT'   :   'A timeout occurred; Possible connection interruption/misconfigured.',
- 'CONNERR'   :   'Error while connecting to host; interruption concerned',
- 'HTTPERR'   :   'Error occurred while establishing connection. Check the connection and retry; If the problem persists, please file an issue along with content of "stack" object.',
- 'EXP_ERR'   :   'Invalid maximum expiration time (must be no more than 30 mins)',
- 'EXPIRED'   :   'The MyBK session has expired. Please do the login again',
- 'ERR_INP'   :   'Recieved no/invalid value(s) when expected. Check "stack" object for what is/are missing/needed'

These error codes can also be returned via the funtions (specifically: `login`, `logout`).

## License
This library has a GNU GPLv3 license

## Future
- Complete the documentation for this library

## FAQ
-	**Q:** **_Can I use non-HCMUT account with this library?_**

	**A:** **No**. As stated above, you can only use account that can access HCMUT MyBK Portal.
-	**Q:** **_How does this library works?_**

	**A:** This library uses _requests_ to mimic the behavior when doing the same thing from the browser. The _html2json_ is used during the request to parse html respond in order to get key component for the success of this crawling proccess.
-	**Q:** **_Why don't you use BeautifulSoup?_**

	**A:** **_BeautifulSoup was obsoleted as from Python 3.2!_** That's why I uses html2json for parsing html output from the request. _(proof: Google it)_
-	**Q:** **_Can you show me how to create something like this?_**

	**A:** **_USE GOOGLE!_** I can't guide you with that, but you can have my code as a reference.
