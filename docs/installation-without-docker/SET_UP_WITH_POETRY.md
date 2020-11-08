# Cài đặt poetry

Làm theo hướng dẫn của [poetry](https://python-poetry.org/docs/) đề cài đặt `poetry` vào máy của bạn

## Cài đặt môi trường (cần chạy lần đầu, các lần sau bỏ qua bước này)

- Để caì đặt toàn bộ dependencies (bao gồm cả development dependencies)
```
$ poetry install
```

- Nếu chỉ muốn cài đặt những dependencies chính cho production
```
$ poetry install --no-dev
```

## 3. Sử dụng poetry:

Hơi giống với `pipenv`, `poetry` mặc định cài đặt cho bạn môi trường ảo sau khi chạy lện `install`. Để kiểm tra 
config setting mặc định của `poetry`, chạy:
```
$ poetry config --list
```  
Tham khảo [documentation](https://python-poetry.org/docs/configuration/) của `poetry` để tự customize nếu muốn.

Dùng các command của framework như bình thường:
Ví dụ:

```
$ python manage.py migrate
```

**Cài đặt thêm thư viện**
```
$ poetry add <library>
```

Tham khảo thêm [documentation](https://python-poetry.org/docs/configuration/)