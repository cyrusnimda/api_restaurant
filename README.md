## Synopsis

This is a restaurant API, to manage bookings, tables, users, etc.
The API is live in my website https://apirestaurant.cyrusnimda.com

## Code Example

Wellcome response:

    curl -i -X GET https://apirestaurant.cyrusnimda.com/

List of tables:

	curl -i -X GET https://apirestaurant.cyrusnimda.com/tables

Get table by id:

	curl -i -X GET https://apirestaurant.cyrusnimda.com/tables/1

Log in:

    curl -i -X POST -d '{"username":"xxxxx", "password": "xxxxx"}' https://apirestaurant.cyrusnimda.com/login

Bookings for today (token needed):

    curl -i -H "x-access-token:xxxxxxxxxxxxxxxxxxxxxx" -X GET https://apirestaurant.cyrusnimda.com/bookings/today


## Motivation

This is just an example of things that can be done with flask.

## Installation

    pip install -r requeriments;
    cp api/config_example.py api/config.py

edit config file with database info(mysql or another one.)

    python console.py init_database
    python api/main.py

## Tests

All tests have a clean database totally isolated than the production one.

    python console.py run_tests