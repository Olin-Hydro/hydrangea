# Contribute

<hr>

### Packages

This API is built using FastAPI, a framework for building modern Python APIs.
See their [website](https://fastapi.tiangolo.com/) for more information and some
great tutorials. For our database we are using
[MongoDB](https://www.mongodb.com/). MongoDB has a great python library called
PyMongo that we are using to interact with the databse.

The app is split into models and routes. The models define the structure of the
data we want to store. This helps us have a standard format in our database and
allows us to marshal the data when we receive it. Built on top of these models
are our routes. These routes define the urls that are available from our api as
well as what methods can be used on them.

### Running Locally with MongoDB Atlas URI

To setup, make sure you have python and pip installed.

Instantiate a [virtual environment](https://docs.python.org/3/library/venv.html)
named venv if the venv folder does not exist. Make sure you activate it.

Download
[Mongodb](https://www.mongodb.com/docs/manual/administration/install-community/)
and optionally mongosh.

To run locally, you need 3 environmental variables:

```
DB_NAME=
ATLAS_URI=<cluster url>
```

You can store these in a `.env` file in the hydrangea home directory. After
following the next steps, you will have a cluster url.

These will run the API with a local database. To run database online, setup a
[MongoDB Atlas URI connection string.](https://www.mongodb.com/docs/atlas/getting-started/)
Follow through the steps under Atlas UI (or Atlas CLI). After you create a
cluster, you will set your `ATLAS_URI` to your cluster url.

### Getting Started

Download all required python packages using `pip install -r requirements.txt`

To use our linting and autoformatting, install the pre-commit packages using
`pre-commit install`

Run linting and commit tests using `pre-commit run --all-files` at any time.
They should run automatically on commit.

To run the API from root directory, run

```
uvicorn app.main:app --port 8000 --reload
```

Navigate to /docs to view all our routes and examples.

To run unit tests:

```
python3 -m pytest
```

## Unit Testing

If you want to contribute, make sure to test all of your schema/routes in tests/
before submitting a PR.
