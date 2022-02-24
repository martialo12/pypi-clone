# PYPI_CLONE

This is a simple clone of [PYPI](https://pypi.org/) web application.

## Features

- **FastAPI** with Python 3.9
- Sqlite
- postgresql
- SqlAlchemy
- Docker compose for easier development
- Simple authentication workflow
- Dependency Injection architecture
- async await code
- Docker compose

## Usage

That was enough talking, how can you use it:

### without docker

Make sure you have [python3.9](https://www.python.org/) installed.

inside pypi-clone folder run:

```
    pip install -r requiirements.txt
```

after ding so run:

```
    uvicorn application:pypi_app --host 0.0.0.0 --port 5000 --reload
```



### with docker

Start pypi_clone application with `docker-compose`.

run this command below inside pypi_clone directory:

```
docker-compose up
```

You can now navigate to `localhost:5000` in your browser and you should be able to see an awesome pypi_clone web application.
At `localhost:5000/docs` or `localhost:5000/redoc` you can inspect the API documentation


## Don't forget the extra steps

Now, edit the configuration file in order to change default values...

```
# configuration
PROJECT_NAME = <get this from your PWC dev account>
AUTH_COOKIE_NAME = <get this from your PWC dev account>
CONFIG_FILE = <get this from your google dev account>

```


## Project Layout
```
pypi-clone
|__ app
|    |
|    |___auth
|    |    |____endpoints.py
|    |    |____repositories.py
|    |    |____schemas.py
|    |    |____services.py
|    |
|    |___user
|    |    |_____endpoints.py
|    |    |_____models.py
|    |    |_____repositories.py
|    |    |_____schemas.py
|    |    |_____services.py
|    |
|    |___package
|    |    |_____endpoints.py
|    |    |_____models.py
|    |    |_____repositories.py
|    |    |_____schemas.py
|    |    |_____services.py
|    |
|    |___release
|    |    |_____endpoints.py
|    |    |_____models.py
|    |    |_____repositories.py
|    |    |_____schemas.py
|    |    |_____services.py
|    | 
|    |___core
|    |    |______config.py
|    |    |------logging.ini
|    |    |______viewmodels
|    |    |       |_________base_viewmodel.py
|    |    |       |_________account_viewmodel.py
|    |    |       |_________details_viewmodel
|    |    |       |_________index_viewmodel
|    |    |       |_________login_viewmodel
|    |    |       |_________register_viewmodel
|    |    |
|    |    |______cookies
|    |            |_________cookie_auth.py
|    |
|    |
|    |___db
|    |    |_____database.py
|    |    |_____test.db
|    |
|    |
|    |___containers.py
|    |---requirements.txt
|
|--application.py
|--docker-compose.yml
|--Dockerfile
|--README.md


```

## Acknowledgements
Special thanks to **Sebastian Ramirez** for his awesome work in the [FastApi](https://fastapi.triangolo.com/) project and to all those who contributed.

Special thanks to **Roman Mogylatov** for his awesome work in the [Dependency Injection](https://python-dependency-injector.ets-labs.org/) framework for Python.

## Authors
Martial wafo

















