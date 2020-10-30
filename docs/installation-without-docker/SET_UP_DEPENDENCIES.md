# Cài đặt các yêu cầu tiên quyết

Chú ý: Nếu bạn chọn cách sử dụng `venv` như hướng dẫn trong tệp [`docs/installation-without-docker/SET_UP_VIRTUALENV.md`](/docs/installation-without-docker/SET_UP_VIRTUALENV.md), hãy bật `venv` khi thực hiện bất cứ lệnh nào dưới đây.

Chú ý: Nếu bạn chọn cách sử dụng `pipenv` như hướng dẫn trong tệp [`docs/installation-without-docker/SET_UP_PIPENV.md`](/docs/installation-without-docker/SET_UP_PIPENV.md), hãy bật môi trường `pipenv` khi thực hiện bất cứ lệnh nào dưới đây.

## 1. Đảm bảo đã cài Python và Node

Hãy đảm bảo rằng bạn đã cài Python 3.6 trở lên.

Kiểm tra như sau:

```
$ python -V
Python 3.8.5
```

Hãy đảm bảo rằng bạn đã cài `node` và `npm`.

Kiểm tra như sau:

```
$ node -v
v12.16.3

$ npm -v
6.14.4
```

## 1. Thỏa mãn requirements.txt

```
$ pip install -r requirements.txt
```

## 2. Thoả mãn package.json

```
$ npm install
```
