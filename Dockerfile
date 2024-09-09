 FROM node:14

 # Install Python
 RUN apt-get update && apt-get install -y python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*2

 WORKDIR /code

 # Node and webpack
 RUN apt-get update -qq && \
     apt-get install -y --no-install-recommends vim curl gnupg && \
     apt-get clean && \
     rm -rf /var/lib/apt/lists/*
 RUN curl -sL https://deb.nodesource.com/setup_12.x  | bash -
 RUN apt-get install -y --no-install-recommends nodejs && \
     apt-get clean && \
     rm -rf /var/lib/apt/lists/*

 COPY ./requirements/base.txt /code/base.txt
 COPY ./requirements/development.txt /code/development.txt
 COPY ./requirements/testing.txt /code/testing.txt

 RUN pip3 install -r /code/development.txt --no-cache-dir
 RUN pip3 install -r /code/testing.txt --no-cache-dir

 ADD package.json package-lock.json ./
 RUN npm install

 # ENV should be configure from outside
 # @see docker-compose.yaml
 ENV DB_NAME cuuhomientrung
 ENV DB_USER cuuhomientrung
 ENV DB_PASSWORD cuuhomientrung
 ENV DB_HOSTNAME localhost
 ENV DB_PORT 5432
 ENV PYTHONUNBUFFERED=1

 ADD . /code/
 RUN npm run build

 RUN chmod +x *.sh
 # Helpers making development easier
 RUN echo "#!/bin/bash\ncd /code\npython project/manage.py runserver_plus 0.0.0.0:8087" > /usr/bin/rs && \
     chmod +x /usr/bin/rs

 CMD ["bash", "-c", "tail -f /dev/null"]
 EXPOSE 8087/tcp
