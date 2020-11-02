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
RUN npm install
RUN npm run build

# ENV should be configure from outside
# @see docker-compose.yaml
ENV DB_NAME cuuhomientrung
ENV DB_USER cuuhomientrung
ENV DB_PASSWORD cuuhomientrung
ENV DB_HOSTNAME localhost
ENV DB_PORT 5432
ENV PYTHONUNBUFFERED=1

ADD . /code/
RUN chmod +x *.sh
# Helpers making development easier
RUN echo "#!/bin/bash\ncd /code\npython project/manage.py runserver_plus 0.0.0.0:8087" > /usr/bin/rs && \
    chmod +x /usr/bin/rs

CMD ["bash", "-c", "tail -f /dev/null"]
EXPOSE 8087/tcp