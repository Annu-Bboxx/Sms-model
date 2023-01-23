
FROM python:3.9.12

COPY requirements.txt requirements.txt
RUN mkdir -p /app

COPY ./ /app/
RUN apt-get upgrade \
&& apt-get update \
&& pip install --upgrade pip
RUN cd /app
RUN cd /app \ && pip install -r requirements.txt
RUN apt-get install libgomp1
RUN apt-get install -y python3-psycopg2

EXPOSE 8080

WORKDIR /app

ENTRYPOINT ["python3","./src/pipelines/predict_model.py"]
