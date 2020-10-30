# Cài đặt database

Đây là hướng dẫn cách cài đặt cơ sở dữ liệu.

Quá trình cài đặt được thử nghiệm trên Ubuntu 20.04. Đối với các hệ điều hành khác, các bạn có thể làm tương tự.

## 1. Cài PostgreSQL

```
$ sudo apt install postgresql postgresql-contrib
```

Tham khảo:

- https://www.postgresql.org/download/

- https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-18-04

## 2. Tạo user, database

Để tạo user `my_user` với password `my_password` và database `my_db`, chạy các lệnh sau:

```
$ sudo -u postgres createuser my_user
$ sudo -u postgres psql -c "ALTER USER my_user WITH PASSWORD 'my_password';"
$ sudo -u postgres psql -c "ALTER USER my_user WITH SUPERUSER"
$ sudo -u postgres createdb my_db
```

Tham khảo:

https://medium.com/coding-blocks/creating-user-database-and-adding-access-on-postgresql-8bfcd2f4a91e

## 3. Chuẩn bị tệp .env

Tạo tệp `.env` với nội dung như sau:

```
DB_NAME=my_db
DB_USER=my_user
DB_PASSWORD=my_password
DB_HOSTNAME=localhost
```

## 4. Tạo schema

```
$ bash run_migrate.sh
```

Về bản chất, lệnh này tương đương với:

```
$ cd project
$ python3 manage.py makemigrations
$ python3 manage.py migrate
```

## 5. Tạo tài khoản admin

Tạo tài khoản `user1` với mật khẩu tùy ý bằng cách chạy:

```
$ bash run_create_admin.sh
```

Về bản chất, lệnh này tương đương với:

```
$ cd project
$ python3 manage.py createsuperuser
```
