# Hydrangea 💐

Newest data api for hydroponics.

# Purpose
This API is meant to be used as part of a scalable automated hydroponics system for Olin College.

It's purpose is to hold information on all gardens and their associated sensors/actuators, as well as configurations (ex. what actuators should trigure at what times). It will also serve as a history log for all sensor readings/actuator actions that actually took place.

It will mainly interact with [mother nature](https://github.com/Olin-Hydro/mother-nature), which processes configurations into simpler commands to send to sensors and actuators, and [saffron](https://github.com/Olin-Hydro/saffron) a frontend dashboard to display garden statuses.

# Interact
To run in Docker using Docker-Compose, clone this repository and run `docker-compose build` and `docker-compose up`. You may have to shut off activity on port 80 beforehand. Alternatively, you can build and run using Docker: `docker build -t <docker_id/<application-name>` and `docker run -p 80:8000 <docker_id>/<application name> `

# CD and Documentation
This repo is currently setup to have continuous deployment to an AWS ECS using AWS Elastic Beanstalk. [API URL](http://hydroapi-env.eba-p7wttzu3.us-east-1.elasticbeanstalk.com/).

To use the API with the official MongoDB atlas database, or check out current API state/documentation, go [here](http://hydroapi-env.eba-p7wttzu3.us-east-1.elasticbeanstalk.com/docs).


# Contribution
To contribute, please read <b>Contribute.md<b>