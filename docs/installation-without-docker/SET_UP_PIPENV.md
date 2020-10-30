# Cài đặt pipenv

## 1. Chuẩn bị môi trường pipenv

```
$ pipenv shell
```

## 2. Cài đặt môi trường pipenv (cần chạy lần đầu, các lần sau bỏ qua bước này)

```
$ pipenv install
```

## 3. Sử dụng pipenv:

Dùng các command của framework như bình thường:
Ví dụ:

```
$ python manage.py migrate
```

Hoặc chạy chực tiếp 1 command của framework mà không cần active venv:
Ví dụ:

```
$ pipenv run python manage.py migrate
```
