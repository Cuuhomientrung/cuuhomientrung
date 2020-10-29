# Cài đặt bằng Docker

## Cài docker và docker-compose

Cài docker theo hướng dẫn tại [đây](https://docs.docker.com/engine/install/ubuntu/)

Cài docker-compose theo hướng dẫn tại [đây](https://docs.docker.com/compose/install/)

Chạy trên local:

```
docker-compose up -d --build
```

## Cài đặt database cho lần đầu

```
docker exec -it cuuhomientrung-web bash
bash run_migrate.sh
bash run_create_admin.sh ## Create with username: `user1`
```

## Truy cập trang

```
localhost:8087
```

## Mẹo: Lệnh truy cập vào cửa sổ dòng lệnh của docker

```
docker exec -it cuuhomientrung-web bash
```
