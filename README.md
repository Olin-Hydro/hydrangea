# Hydrangea 💐

Newest data api for hydroponics.

# Purpose

This API is meant to be used as part of a scalable automated hydroponics system
for Olin College.

It's purpose is to hold information on all gardens and their associated
sensors/actuators, as well as configurations (ex. what actuators should trigure
at what times). It will also serve as a history log for all sensor
readings/actuator actions that actually took place.

It will mainly interact with
[mother nature](https://github.com/Olin-Hydro/mother-nature), which processes
configurations into simpler commands to send to sensors and actuators, and
[saffron](https://github.com/Olin-Hydro/saffron) a frontend dashboard to display
garden statuses.

# Deployment

This app is deployed as an aws lambda function. This lambda function is called
whenever an API gateway call is made. For instructions on this setup and further
information see
[this tutorial](https://towardsdatascience.com/fastapi-aws-robust-api-part-1-f67ae47390f9).

The latest code will be uploaded to our lambda function whenever a new tagged
release is created in github.

# Contribution

To contribute, please read <b>CONTRIBUTE.md<b>
