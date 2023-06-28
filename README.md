# Event Manager
Django and DRF app for managing events. It should allow users to create a personal account, log in, and create, edit, 
fetch, and register to attend events. Each event should have at least a name, a description, a start date and end date 
and a list of attendees.

Main features of the project:
- A system of token rotation is implemented. For this the API provides a user with access_token and a refresh_token, 
as well as a way to refresh and validate the access_token. The lifetime of the access_token is 1 hour and the lifetime 
of the refresh_token 1 day
- API docs (swagger or other)
- tests
- Users are able to register an account
- Users are able to log in into their account
- Users are able to create events in the app's database (slqlite)
- Users are able to see the list of events they have created
- Users are able to see a list of all events
- Users are able to edit the events they have created but not the ones created by other users
- Users are able to register to an event or un-register. This can only be done in future events and not in past events.
- Logic to manage an event capacity: if event reaches maximum number of registered attendees, an error is be returned 
to a user trying to register

Things that this project does not implement:
- Documentation of the code
- Filtering to endpoints retrieving events (e.g. date , type, status, past events, future events, etc)
- Frontend to consume the API


## SetUp

It's highly suggested that you create a virtual environment for running this app. Typical IDE's (like PyCharm) should
help you do this automatically.

After creating the virtual env and activating it please install all the requirements:

```bash
pip install -r requirements.txt
```

Creating DB migrations:

```bash
python manage.py makemigrations
```

Running migrations created in the preceding step:

```bash
python manage.py migrate
```

Creating superuser for the app:

```bash
python manage.py createsuperuser
```

Running the app locally:

```bash
python manage.py runserver
```
 
Running tests:

```bash
python manage.py test
```

Swagger docs are available (locally with default host and port): http://127.0.0.1:8000/swagger/