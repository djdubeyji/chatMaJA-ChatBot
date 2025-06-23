# images: https://hub.docker.com/_/python/tags?page=1&name=3.11
FROM python:3.11.8-bullseye

# arbitrary directory name, inside the container
WORKDIR /app

# copy from this directory to /app in the container all files according to .dockerignore
COPY . /app

# important to cache pip dependencies
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

EXPOSE 5000

# for saving models downloaded from huggingface to this folder automatically
ENV HF_HOME=/app/models
# LanceDB was showing errors when trying to save to /root/ folder
ENV LANCEDB_CONFIG_DIR=/app/db_config

# for Flask to know which file to run (default is app.py)
ENV FLASK_APP=app

# --host allows acessing Flask in Docker container from any address, including localhost
CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0"]
