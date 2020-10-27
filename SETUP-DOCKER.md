# Instruction how to set it up on your local and contribute to the project

## Installation

### Install Docker ENV + docker-compose (recommend)
1. Install docker from (here)[https://docs.docker.com/engine/install/ubuntu/]
2. Install docker-compose from (here)(https://docs.docker.com/compose/install/)
### Run on local
```
docker-compose up -d --build
```

### Config database

### First time - Set it up
```
docker exec -it cuuhomientrung-web bash
bash run_migrate.sh
bash run_create_admin.sh ## Create with username: `user1`
```

### Open on browser
```
localhost:8087
```


### Next time, access to docker-container
```
docker exec -it cuuhomientrung-web bash
```
