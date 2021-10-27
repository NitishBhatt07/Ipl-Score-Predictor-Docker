FROM python:3.8.8

COPY . /usr/app

EXPOSE 3000

WORKDIR /usr/app 

RUN pip install -r requirements.txt

CMD python app.py