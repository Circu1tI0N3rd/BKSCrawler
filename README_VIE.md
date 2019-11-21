
# BKSCrawler

## Đây là gì?
 Đây là thư viện cho Python được viết dựa trên 2 nguồn:
  - Các gói thông tin từ Wireshark,
  - Và code của _PythonTryHard_: [BKSchedule_Rewrite](https://github.com/PythonTryHard/BKSchedule_Rewrite)

Thư viện dùng **2** thư viện phụ: [_html2json_](http://pypi.org/project/html2json/) và [_requests_](https://pypi.org/project/requests/) (both in Python).

Khi được cung cấp _username_ và _password_, thư viện trả về chuỗi JSON có thể là:
- Lịch học nếu mọi thứ suông sẻ,
- Hoặc lỗi nếu có.

Tài khoản dùng trên phải truy cập được [MyBK](https://mybk.hcmut.edu.vn).
 
## Mục tiêu chính
- Khắc phục 1 số lỗi của BKSchedule_Rewrite gốc;
- Thêm request logout ngay sau khi lấy được thời khoá biểu;
- Cho mọi người tự quyết việc mình muốn hiển thị thời khoá biểu như thế nào.

## Basic usage
Cho rằng bạn đang ở màn hình lệnh của Python 3.7 và đã cài thư viện cần thiết:

	python3 pip install requests html2json

### Input:

    >>> from BKSCrawler import get_timetable
    >>> get_timetable(<Your username here>, <Your password here>)

### Output:
Thành công:

    {'http' : 0, 'code' : [<...Timetable array here...>]}

Sai thông tin đăng nhập hay bất kỳ vấn đề liên quan đến website:

    {'http' : <Any code NOT 302>, 'code' : '<Respond from the website>}'

Lỗi khi chạy:

    {'http' : 666, 'code' : '<The stacktrace in string>'}

## Bản quyền
Thư viện này sử dụng GNU GPLv3.

## Tương lai
- Sử dụng hashing với khoá cho mật khẩu thay vì nhập mật khẩu trực tiếp vào function (hiện tại chưa hỗ trợ).

## FAQ
-	**Q:** **_Tôi có thể sử dụng tài khoản không phải của MyBK?_**

	**A:** **KHÔNG**. Như đã khẳng định ở trên, thư viện chỉ sử dụng được tài khoản MyBK.
-	**Q:** **_Nguyên tắc hoạt động?_**

	**A:** Thư viện sử dụng _requests_ để giả lập hành động tương tự như thao tác trên trình duyệt web. _html2json_ được sử dụng trong quá trình yêu cầu để lấy thông tin cần thiết từ respond của web.
-	**Q:** **_Sao không sử dụng BeautifulSoup?_**

	**A:** **_BeautifulSoup đã lỗ thời từ Python 3.2!_** Đó là lý do của việc sử dụng _html2json_. _(proof: Google)_
-	**Q:** **_Tôi muốn làm thư viện tương tự?_**

	**A:** **_DÙNG GOOGLE!_** Tôi không thể hướng dẫn bạn, như bạn có thể sử dụng code của tôi như code mẫu.
