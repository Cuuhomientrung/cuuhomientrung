FROM python:3
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

ADD requirements.txt .
RUN pip install -r requirements.txt

ADD package.json package-lock.json ./
RUN npm instal

# ENV should be configure from outside
# @see docker-compose.yaml
ENV DB_NAME cuuhomientrung
ENV DB_USER cuuhomientrung
ENV DB_PASSWORD cuuhomientrung
ENV DB_HOSTNAME localhost
ENV DB_PORT 5432

ADD . /code/
RUN chmod +x *.sh

CMD ["bash","-c","env > .env && ./run_server.sh"]
