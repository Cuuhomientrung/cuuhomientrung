# Cài đặt virtualenv

Trước khi làm bước này, hãy đảm bảo rằng bạn đã cài Python 3.6 trở lên.

## 1. Tạo thư mục venv

Tại thư mục gốc của dự án (thư mục `cuuhomientrung`), chạy lệnh sau:

```
$ python3 -m venv venv
```

Lệnh vừa rồi sẽ tạo thư mục `venv` trong thư mục `cuuhomientrung`.

Tham khảo:

- https://docs.python.org/3/library/venv.html

## 2. Bật/tắt venv

Tại thư mục gốc của dự án (thư mục `cuuhomientrung`), chạy lệnh sau:

Bật venv:

```
$ source venv/bin/activate
```

Kiểm tra:

```
$ pip -V

pip 20.0.2 from /.../.../.../cuuhomientrung/venv/lib/python3.8/site-packages/pip (python 3.8)
```

Tắt venv:

```
$ deactivate
```
