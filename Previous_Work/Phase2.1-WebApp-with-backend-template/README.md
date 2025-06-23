# Updated UI Docker image with template for adding backend

### Contents:
- `app.py` - starting point, Flask app at http://127.0.0.1:5000/
- `Dockerfile` - to build an image with the app
- `requirements.txt` - Python packages required by the app and installed to the container when building an image
- `docker-compose.yml` - to build an image and start a container with the app
- `qa_pipeline.py` - a **template for adding a backend** to the Flask frontend app.


## How to run - Python / Docker / Docker Compose

> **Note:** commands below assume you're in the directory with the `app.py`, `Dockerfile` and `docker-compose.yml` files.

### Locally - with Flask and Python

Also for easy development of UI due to auto-reload feature.

```bash
python app.py
# or 
flask run --debug
```
Then, open http://127.0.0.1:5000/ in a web browser. 

#### More details

Flask docs about command line options: [here](https://flask.palletsprojects.com/en/3.0.x/cli/#application-discovery).

By default, the app runs on port 5000. **To change the port** to `5001`, set the `FLASK_RUN_PORT` environment variable ([examples](https://flask.palletsprojects.com/en/3.0.x/cli/#setting-command-options)) OR an add additional argument `--port 5001` to the `flask run` command.
```bash
flask run --port 5001 --debug
```

To trigger **auto-reload on additional file changes**, see [Flask cli docs](https://flask.palletsprojects.com/en/3.0.x/cli/#watch-and-ignore-files-with-the-reloader).

### Locally - with Docker

Build an image based on Dockerfile, then start a container from the image.

```bash
docker build -t chatmaja:v1 .
docker run -p 5000:5000 chatmaja:v1
```

Then, open http://127.0.0.1:5000/ in a web browser.

#### More details

When building an image, you can set different tags with `-t` option. The tag `chatmaja:v1` is just an example. 

You can change port the app is available in your local browser by changing the first port number in the `-p` option. For example, to run the app on port 5001, use `-p 5001:5000`. Note, that port number used by the container itself will remain `5000` which might be misleading when reading logs.

### Locally - with Docker Compose

The easiest way.

```bash
docker compose up -d
```

Then, open http://localhost:5000/.

#### More details

To see logs, start the app without `-d`:
```bash
docker compose up
```

The docker compose builds an image based on the Dockerfile in the current directory, tags the image as `chatmaja/v1` and starts a container. Port 5000 of the container is mapped to port 5000 of the host, so the http://localhost:5000/ works as expected.

## TODO

- Add backend to the template app.
- Add caching of building the docker image if builds time got too long.