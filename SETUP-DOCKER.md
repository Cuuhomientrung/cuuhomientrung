# Set up a local DEV environment with Docker

## Install docker + docker-compose

- Install [docker](https://docs.docker.com/engine/install/)
- Install [docker-compose](https://docs.docker.com/compose/install/)

## Set up the DEV environment

```shell
# replace the repo with your fork
git clone https://github.com/Cuuhomientrung/cuuhomientrung
cd cuuhomientrung
docker-compose up -d --build
```

To access the DEV environment, run:

```shell
docker exec -it cuuhomientrung-web bash
```

## Config the database (first time only)

Within the DEV environment, run:

```shell
bash run_migrate.sh
bash run_create_admin.sh ## Create with username: `user1`
```

## Start the DEV server

```shell
bash run_server.sh
```

The DEV server is listening at http://localhost:8087.
