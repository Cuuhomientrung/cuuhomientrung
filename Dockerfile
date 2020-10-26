FROM python:3
WORKDIR /code
ADD requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt &&\
    pip install django-select2-admin-filters
ADD . /code/
RUN chmod +x *.sh
ENV DB_NAME cuuhomientrung
ENV DB_USER cuuhomientrung
ENV DB_PASSWORD cuuhomientrung
ENV DB_HOSTNAME localhost
ENV DB_PORT 5432
ENTRYPOINT ["bash","-c","env > .env && ./run_server.sh"]
