
# BKSCrawler
***Dear beta testers!*** A class-oriented version of this library is available on branch "Classalistic"!

## What is this?
 This is a Python library I wrote based on the following 2 sources:
  - Packet capturing from Wireshark,
  - And _PythonTryHard_'s [BKSchedule_Rewrite](https://github.com/PythonTryHard/BKSchedule_Rewrite)

The library uses **2** additional libraries: [_html2json_](http://pypi.org/project/html2json/) and [_requests_](https://pypi.org/project/requests/) (both in Python).

When supplied with _a username_ and _a password_, the library produces a JSON-formatted output which can be either:
- The schedule if everything is running smooth,
- Or the error code with value if there's anything wrong.

The credential information above must be able to access [HCMUT MyBK Portal](https://mybk.hcmut.edu.vn).
 
## Main aims
- Fixes some issues with the original BKSchedule_Rewrite above;
- Adding a logout method;
- Letting others the possiblity to propagates the tables for their tastes.

## Basic usage
Assuming you are in Python 3.7 shell and already install all requirements:

	python3 pip install requests html2json

### Input:

    >>> from BKSCrawler import get_timetable
    >>> get_timetable(<Your username here>, <Your password here>)

### Output:
Success:

    {'http' : 0, 'code' : [<...Timetable array here...>]}

Invalid credential or other web-related issues:

    {'http' : <Any code NOT 302>, 'code' : '<Respond from the website>}'

Exceptions:

    {'http' : 666, 'code' : '<The stacktrace in string>'}

## License
This library has a GNU GPLv3 license

## Future
- Use hashing with key for password instead of plain text when inputing to funtion (Currently not supported).

## FAQ
-	**Q:** **_Can I use non-HCMUT account with this library?_**

	**A:** **No**. As stated above, you can only use account that can access HCMUT MyBK Portal.
-	**Q:** **_How does this library works?_**

	**A:** This library uses _requests_ to mimic the behavior when doing the same thing from the browser. The _html2json_ is used during the request to parse html respond in order to get key component for the success of this crawling proccess.
-	**Q:** **_Why don't you use BeautifulSoup?_**

	**A:** **_BeautifulSoup was obsoleted as from Python 3.2!_** That's why I uses html2json for parsing html output from the request. _(proof: Google it)_
-	**Q:** **_Can you show me how to create something like this?_**

	**A:** **_USE GOOGLE!_** I can't guide you with that, but you can have my code as a reference.
