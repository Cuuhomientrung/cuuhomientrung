FROM python:3
WORKDIR /code

# Node and webpack
RUN apt-get update
RUN apt-get install -y vim
RUN apt-get install curl
RUN apt-get -y install curl gnupg
RUN curl -sL https://deb.nodesource.com/setup_11.x  | bash -
RUN apt-get -y install nodejs
RUN npm install -g yarn
RUN yarn

# Install python requirement
ADD requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt

#Add code to image
ADD . /code/
RUN chmod +x *.sh 

#Run necessary build
RUN npm install &&\
    npm run build

# ENV should be configure from outside
# @see docker-compose.yaml
ENV DB_NAME cuuhomientrung
ENV DB_USER cuuhomientrung
ENV DB_PASSWORD cuuhomientrung
ENV DB_HOSTNAME localhost
ENV DB_PORT 5432

CMD ["bash","-c","env > .env && ./run_server.sh"]
