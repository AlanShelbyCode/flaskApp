FROM python:3.8.12

WORKDIR /application

COPY ./requirements.txt /application/requirements.txt
COPY ./wait-for-it.sh /application/wait-for-it.sh


RUN pip install -r requirements.txt


CMD ./wait-for-it.sh db:3306 -- python3 app.py

#CMD python3 app.py
#CMD flask run --host=0.0.0.0 --port=8080