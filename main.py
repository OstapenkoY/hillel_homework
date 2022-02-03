import datetime
import pprint
import random
import string

import requests
from flask import Flask, request, jsonify, Response

from http import HTTPStatus

from database_handler import execute_query

from webargs import validate, fields
from webargs.flaskparser import use_kwargs

from utils import format_records

app = Flask(__name__)


@app.errorhandler(HTTPStatus.UNPROCESSABLE_ENTITY)
@app.errorhandler(HTTPStatus.BAD_REQUEST)
def error_handling(error):
    headers = error.data.get("headers", None)
    messages = error.data.get("messages", ["Invalid request."])

    if headers:
        return jsonify(
            {
                'errors': messages
            },
            error.code,
            headers
        )
    else:
        return jsonify(
            {
                'errors': messages
            },
            error.code,
        )


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/hello")
def hello():
    print('testd')
    return "<p>Hello, Mykhailo!</p>"


@app.route("/now")
def get_current_time():
    return f"{datetime.datetime.now()}"


@app.route("/generate-password")
@use_kwargs(
    {
        "length": fields.Int(
            missing=10,
            validate=[validate.Range(min=8, max=100)]
        ),
    },
    location="query"
)
def generate_password(length):
    return "".join(
        random.choices(
            string.ascii_lowercase + string.ascii_uppercase,
            k=length
        )
    )


@app.route("/get-astronauts")
def get_astronauts():
    url = "http://api.open-notify.org/astros.json"
    result = requests.get(url, {})

    if result.status_code not in (HTTPStatus.OK,):
        return Response("ERROR: Something went wrong",
                        status=result.status_code)

    result = result.json()
    statistics = {}
    for entry in result.get('people', {}):
        statistics[entry['craft']] = statistics.get(entry['craft'], 0) + 1

    pprint.pprint(statistics)

    return statistics


@app.route("/customers")
@use_kwargs(
    {
        "first_name": fields.Str(
            required=False,
            missing=None,
            validate=[validate.Regexp("^[0-9]*")]
        ),
        "last_name": fields.Str(
            required=False,
            missing=None,
            validate=[validate.Regexp("^[0-9]*")]
        )
    },
    location="query"
)
def get_all_customers(first_name, last_name):
    query = "SELECT * FROM customers"

    fields = {}

    if first_name:
        fields["FirstName"] = first_name

    if last_name:
        fields["LastName"] = last_name

    if fields:
        query += " WHERE " + " AND ".join(
            f"{key}=?" for key in fields.keys()
        )

    records = execute_query(query=query, args=tuple(fields.values()))

    return format_records(records)


def order_price():
    #  UnitPrice * Quantity - show on page.
    #  Add possibility to get data by Country
    # by default all countries
    # join two tables invoices and invoices_items
    pass


def get_all_info_about_track():
    # join all possible tables and show all possible
    # info about all tracks
    pass


def get_all_info_about_track():
    # *
    # show time of all tracks of all albums
    # info about all tracks
    pass


app.run(port=5001, debug=True)
