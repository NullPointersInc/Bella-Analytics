# Bella-Middleware

Contains the middleware code for Bella that includes user, device, and room management, as well as analytics.

## Prerequisites

1. Ensure that the following **python3** packages are installed, as this project runs on python3:
* django
* matplotlib
* bcrypt

2. You need to setup mysql as defined in `bella_middleware/settings.py`. If you are using different credentials, ensure they are reflected in `settings.py`.

3. Once MySQL is set up, execute `python3 manage.py makemigrations <<appname>>` for every app within the server.

4. Then execute `python3 manage.py migrate`.
5. To run the server, simply execute `python3 manage.py runserver` or `./runserver`.
