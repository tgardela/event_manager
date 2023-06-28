# Event Manager
Django and DRF app for managing events

## SetUp

It's highly suggested that you create a virtual environment for running this app. Typical IDE's (like PyCharm) should
help you do this automatically.

After creating the virtual env and activating it please install all the requirements:

```bash
pip install -r requirements.txt
```



The task consists in creating a Rest API using Django rest framework https://www.django-rest-framework.org/to create an 
Event manager app. It should allow users to create a personal account, log in, and create, edit, fetch, and register to 
attend events. Each event should have at least a name, a description, a start date and end date and a list of attendees.

Required features:

DONE    - Users must be able to register an account

DONE    - Users must be able to log in into their account

DONE    - A system of token rotation must be implemented. For this the API needs to provide a user with access_token and
            a refresh_token, as well as a way to refresh and validate the access_token. The lifetime of the access_token
            should be 1 hour and the lifetime of the refresh_token 1 day

DONE    - Users must be able to create events in the app's database (slqlite)

DONE    - Users must be able to see the list of events they have created

DONE    - Users must be able to see a list of all events

DONE    - Users must be able to edit the events they have created but not the ones created by other users

- Users must be able to register to an event or un-register. This can only be done in future events and not in past events.


Not required but nice to have:

 

- Documentation of your code

DONE    - API docs (swagger or other)

- Tests

- Add logic to manage an event capacity: if event reaches maximum number of registered attendees, an error should be returned to a user trying to register

- Add some  filtering to endpoints retrieving events (e.g. date , type, status, past events, future events, etc)

- Create a frontend to consume the API
