# in-memory-cache

This a simple implementation of an in-memory cache using Flask.

It has been developed using Python 3.9.6 and [Docker](https://www.docker.com/). 

## Configuration

Make a copy of the file ```instance/sample-config.py``` and rename it ```config.py```. Set the configuration parameters as needed

## Running locally without `docker`

First, you probably should create python local environment and activate it.

To run the basic server, you'll need to install a few requirements. To do this, run:

```bash
pip install -r requirements.txt
```

To boot up the server, you can run:

```bash
export APP_ENV=development
python wsgi.py
```  

You should now be able to communicate with server on the url:

```bash
localhost:8080/
``` 

APP_ENV could be any envirement set in your config.py file

## Running with `docker-compose`

You'll need [Docker](https://www.docker.com/products/docker-desktop) 
installed to run this project with docker-compose. To build and launch the containerised app, 
run:

```bash
docker-compose up -d --build
```

You should see your server boot up, and should be accessible as before.

When run with docker-compose, the default environment is development

## Running with `docker`

You'll need [Docker](https://www.docker.com/products/docker-desktop) 
installed to run this project with Docker. To build a containerised version of the API, 
run:

```bash
docker build . -t cache-api
```

To launch the containerised app, run:

```bash
docker run -p 8080:8080 -e APP_ENV=development cache-api
```

You should see your server boot up, and should be accessible as before.

APP_ENV could be any envirement set in your config.py file

## Running the tests

You need to install the requirements. To do this, run:

```bash
pip install -r requirements.txt
```
Then, you run:

```bash
pytest -v
```  
