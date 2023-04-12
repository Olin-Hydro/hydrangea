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

# Using Hydrangea

Hydrangea is deployed at https://hydrangea.kaz.farm. The api is currently secured behind an API key, so going to this URL will result in a 403 error. To view hydrangea provide the ```x-api-key``` header when making requests.

To view a list of all the routes and supported methods, install ModHeader so that you can modify the https headers on your browser: https://chrome.google.com/webstore/detail/modheader-modify-http-hea/idgpnmonknjnojddfkpgkljpfnnfcklj. Next add the ```x-api-key``` header to your browser, and navigate to https://hydrangea.kaz.farm/docs. This will show you the swagger docs for our API and allow you to try out requests.

# Deployment

This app is deployed as an aws lambda function. This lambda function is called
whenever an API gateway call is made. For instructions on this setup and further
information see
[this tutorial](https://towardsdatascience.com/fastapi-aws-robust-api-part-1-f67ae47390f9).

The latest code will be uploaded to our lambda function whenever a new tagged
release is created in github.

# Contribution

To contribute, please read <b>CONTRIBUTE.md<b>
