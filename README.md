# Hydrangea 💐

Newest data api for hydroponics.

## Purpose
This api is meant to be used as part of a scalable automated hydroponics system for Olin College.

It's purpose is to hold information on all gardens and their associated sensors/actuators, as well as configurations (ex. what actuators should trigure at what times). It will also serve as a history log for all sensor readings/actuator actions that actually took place.

It will mainly interact with [mother nature](https://github.com/Olin-Hydro/mother-nature), which processes configurations into simpler commands to send to sensors and actuators, and [saffron](https://github.com/Olin-Hydro/saffron) a frontend dashboard to display garden statuses.

## Interact
To run in Docker using Docker-Compose, clone this repository and run `docker-compose build` and `docker-compose up`. You may have to shut off activity on port 80 beforehand. Alternatively, you can build and run using Docker: `docker build -t <docker_id/<application-name>` and `docker run -p 80:8000 <docker_id>/<application name> `

## CD and Documentation
This repo is currently setup to have continuous deployment to an AWS ECS using AWS Elastic Beanstalk. [API URL](http://hydroapi-env.eba-p7wttzu3.us-east-1.elasticbeanstalk.com/).

To use the API with the official MongoDB atlas database, or check out current API state/documentation, go [here](http://hydroapi-env.eba-p7wttzu3.us-east-1.elasticbeanstalk.com/docs).



<hr>


## Contribute

To setup, make sure you have python and pip installed.

Instantiate a [virtual environment](https://docs.python.org/3/library/venv.html) named venv if the venv folder does not exist. Make sure you activate it.

Download [Mongodb](https://www.mongodb.com/docs/manual/administration/install-community/) and optionally mongosh.

Create a .env file with a database URI and database name. To run the database locally, your env would look like:

```
DB_NAME=pymongo_tutorial
ATLAS_URI=mongodb://localhost:27017/test
```

To run database online, setup a [MongoDB Atlas URI connection string](https://www.mongodb.com/docs/atlas/getting-started/)

Download all required python packages using `pip install -r requirements.txt`

To use our linting and autoformatting, install the pre-commit packages using `pre-commit install`

Run linting and commit tests using `pre-commit run --all-files` at any time. They should run automatically on commit.

To Run API from root directory, run

```
python3 App/main.py
```

To run unit tests: 

```
python3 -m pytest
```

# Schema

These are the final schema layed out for the api to organize the various sensors and actuators, as well as recording actions and readings.

### Sensor

| Name       | Type          |
| ---------- | ------------- |
| id         | `Key`         |
| name       | `String`      |
| garden_id  | `Foreign Key` |
| created_at | `Datetime`    |

### Scheduled Actuators

| Name       | Type          |
| ---------- | ------------- |
| id         | `Key`         |
| name       | `String`      |
| garden_id  | `Foreign Key` |
| created_at | `Datetime`    |

### Reactive Actuators

| Name       | Type          |
| ---------- | ------------- |
| id         | `Key`         |
| name       | `String`      |
| sensor_id  | `Foreign Key` |
| created_at | `Datetime`    |

### Gardens

| Name       | Type                 |
| ---------- | -------------------- |
| id         | `Key`                |
| name       | `String`             |
| config     | `Operational Config` |
| location   | `String`             |
| created_at | `Datetime`           |

# Logging

We will also keep track of the actions that actually took place and readings taken from sensors.

### Readings

| Name       | Type          |
| ---------- | ------------- |
| id         | `Key`         |
| sensor_id  | `Foreign Key` |
| value      | `Float`       |
| created_at | `Datetime`    |

### Scheduled Actions

| Name        | Type          |
| ----------- | ------------- |
| id          | `Key`         |
| actuator_id | `Foreign Key` |
| data        | `String`      |
| created_at  | `Datetime`    |

### Reactive Actions

| Name        | Type          |
| ----------- | ------------- |
| id          | `Key`         |
| actuator_id | `Foreign Key` |
| data        | `String`      |
| created_at  | `Datetime`    |

# Config

The Configurations Table will be used in conjunction with logging data in [Mother Nature](https://github.com/Olin-Hydro/mother-nature)

### Operational Config

| Name                | Type       |
| ------------------- | ---------- |
| id                  | `Key`      |
| name                | `String`   |
| sensors             | `[SS]`     |
| scheduled_actuators | `[SAS]`    |
| reactive_actuators  | `[RAS]`    |
| created_at          | `Datetime` |

### Sensor Schedule (SS)

| Name     | Type          |
| -------- | ------------- |
| S_id     | `Foreign Key` |
| interval | `Float`       |

### Scheduled Actuator Schedule (SAS)

| Name  | Type               |
| ----- | ------------------ |
| SA_id | `Foreign Key`      |
| on    | `Array[Timestamp]` |
| off   | `Array[Timestamp]` |

### Reactive Actuator Schedule (RAS)

| Name           | Type          |
| -------------- | ------------- |
| RA_id          | `Foreign Key` |
| interval       | `Float`       |
| threshold      | `Float`       |
| duration       | `Float`       |
| threshold_type | `Int`         |

Each config will be a list of schedule objects  
Example:

```
  {
    "_id": "635ca8fdbb5a675ed710773a",
    "name": "Config1",
    "scheduled_actuators": [
      {
        "SA_id": "635ca57475e8e2a0afbe1bd5",
        "on": [
          "uu"
        ],
        "off": [
          "vv"
        ]
      }
    ],
    "sensors": [
      {
        "S_id": "635ca57475e8e2a0afbe1bd5",
        "interval": 5
      }
    ],
    "reactive_actuators": [
      {
        "RAS_id": "635ca57475e8e2a0afbe1bd5",
        "interval": 5,
        "threshold": 3,
        "duration": 2,
        "threshold_type": 1
      }
    ],
    "created_at": "2022-10-29T00:15:35.270403"
  }

```

<hr />

# Route Tables

### Sensors

| Verb  | URI Pattern          | Controller Action        |
| ----- | -------------------- | ------------------------ |
| GET   | `/sensors/`          | `view all sensors`       |
| GET   | `/sensors/:sensorId` | `view individual sensor` |
| POST  | `/sensors/`          | `add`                    |
| PATCH | `/sensor/:sensorId`  | `update`                 |

### Scheduled Actuators

| Verb  | URI Pattern | Controller Action              |
| ----- | ----------- | ------------------------------ |
| GET   | `/sa/`      | `view all scheduled actuators` |
| GET   | `/sa/:saId` | `view scheduled actuators`     |
| POST  | `/sa/`      | `add`                          |
| PATCH | `/sa/:saId` | `update`                       |

### Reactive Actuators

| Verb  | URI Pattern | Controller Action             |
| ----- | ----------- | ----------------------------- |
| GET   | `/ra/`      | `view all reactive actuators` |
| GET   | `/ra/:raId` | `view reactive actuators`     |
| POST  | `/ra/`      | `add`                         |
| PATCH | `/ra/:raId` | `update`                      |

<hr />

### Gardens

| Verb  | URI Pattern          | Controller Action                     |
| ----- | -------------------- | ------------------------------------- |
| GET   | `/gardens/`          | `view all gardens`                    |
| GET   | `/gardens/:gardenId` | `view a specific garden` |
| POST  | `/gardens/`          | `add`                                 |
| PATCH | `/gardens/:gardenId` | `update`                              |

<hr />

## Logging

### Sensor

| Verb | URI Pattern                  | Params                                 | Controller Action                                                                               |
| ---- | ---------------------------- | -------------------------------------- | ----------------------------------------------------------------------------------------------- |
| GET  | `/sensors/logging/`          | limit: int,start: ISO8601,end: ISO8601 | `view all sensor readings between start and end time up to limit number of logs`                |
| GET  | `/sensors/logging/:sensorId` | limit: int,start: ISO8601,end: ISO8601 | `view all readings for a specific sensor between start and end time up to limit number of logs` |
| POST | `/sensors/logging/`          |                                        | `add sensor reading`                                                                            |

### Reactive Actions

| Verb | URI Pattern                     | Params                                 | Controller Action                                                                |
| ---- | ------------------------------- | -------------------------------------- | -------------------------------------------------------------------------------- |
| GET  | `/ra/logging/actions/`          | limit: int,start: ISO8601,end: ISO8601 | `view all actions between start and end time and up to limit number of logs`     |
| GET  | `/ra/logging/actions/:actionId` | limit: int,start: ISO8601,end: ISO8601 | `view specific action between start and end time and up to limit number of logs` |
| POST | `/ra/logging/actions/`          |                                        | `add actions`                                                                    |

### Scheduled Actions

| Verb | URI Pattern                     | Params                                 | Controller Action                                                                |
| ---- | ------------------------------- | -------------------------------------- | -------------------------------------------------------------------------------- |
| GET  | `/sa/logging/actions/`          | limit: int,start: ISO8601,end: ISO8601 | `view all actions between start and end time and up to limit number of logs`     |
| GET  | `/sa/logging/actions/:actionId` | limit: int,start: ISO8601,end: ISO8601 | `view specific action between start and end time and up to limit number of logs` |
| POST | `/sa/logging/actions/`          | limit: int,start: ISO8601,end: ISO8601 | `add actions`                                                                    |

## Unit Testing
If you want to contribute, make sure to test all of your schema/routes in App/server/tests before submitting a PR.