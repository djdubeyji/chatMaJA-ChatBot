# images: https://hub.docker.com/_/python/tags?page=1&name=3.11
FROM python:3.11.7-alpine3.19

WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENV FLASK_APP=app

CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0"]
