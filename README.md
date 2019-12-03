
# BKSCrawler
Please note there are some missing information in this README. I am deeply apologize about such manner.

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

    > import BKSCrawler as bk
    > mybk = bk.StInfoCrawl(<Your username here>, <Your NaCl-encrypted password here>)
    > mybk.login([Your NaCl encryption phrase here])

- Get your information (say, timetable) from HCMUT StInfo Portal: `mybk.fetch('sched')`
Return: A Python dictionary type
_Valid commands are:_
  'sched': Get timetable;
  'grade': Get exam gradings;
  'exam': Get exam schedule;
  'msg': Get annoucements available.

- Get current week: `mybk.week`
Return: (integer) this week number

- Log out of the portal: `mybk.logout()`

- Change expiry time of the session: `mybk.setExpire(<time_in_int>, <Format: min|sec>)`
***NOTE:*** The maximum allowed period is ***30 minutes***

## Exceptions
The function will throw `BKSCrawler.CrawlerError` for most errors (specific exceptions do exist) during the crawling process for most commands.

***ADDITIONALLY***, for any value errors (missing/invalid command arguments), `AssertionError` is raised.

## License
This library has a GNU GPLv3 license

## Future
- Expand Exceptions
- Update other language

## FAQ
-	**Q:** **_Can I use non-HCMUT account with this library?_**

	**A:** **No**. As stated above, you can only use account that can access HCMUT MyBK Portal.
-	**Q:** **_How does this library works?_**

	**A:** This library uses _requests_ to mimic the behavior when doing the same thing from the browser. The _html2json_ is used during the request to parse html respond in order to get key component for the success of this crawling proccess.
-	**Q:** **_Why don't you use BeautifulSoup?_**

	**A:** **_BeautifulSoup was obsoleted as from Python 3.2!_** That's why I uses html2json for parsing html output from the request. _(proof: Google it)_
-	**Q:** **_Can you show me how to create something like this?_**

	**A:** **_USE GOOGLE!_** I can't guide you with that, but you can have my code as a reference.
