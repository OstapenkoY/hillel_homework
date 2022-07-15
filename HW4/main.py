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

from utils import format_records, my_format_records

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


@app.route("/order-price")
@use_kwargs(
    {
        "country": fields.Str(
            required=False,
            missing=None,
            validate=[validate.Regexp("^[0-9]*")]
        )
    },
    location="query"
)
def order_price(country):
    query = "SELECT invoices.BillingCountry, round(sum(invoice_items.UnitPrice), 2)  \
                FROM invoice_items \
                JOIN invoices ON invoice_items.InvoiceId = invoices.InvoiceId "
    fields = {}

    if country:
        fields['invoices.BillingCountry'] = country

    if fields:
        query += " AND " + ''.join(f"{key}=?" for key in fields.keys()) + " GROUP BY invoices.BillingCountry;"

        records = execute_query(query=query, args=tuple(fields.values()))
        return format_records(records)
    else:
        query += " GROUP BY invoices.BillingCountry;"

        records = execute_query(query=query, args=tuple(fields.values()))
        return format_records(records)


@app.route("/track-info")
@use_kwargs(
    {
        "id": fields.Str(
            required=False,
            missing=None,
            validate=[validate.Regexp("^[a-zA-Z]*")]
        )
    },
    location="query"
)
def get_all_info_about_track(id):
    query = "SELECT tracks.TrackID, tracks.Composer, tracks.Name AS TrackName, tracks.UnitPrice, \
                    tracks.Milliseconds, tracks.Bytes, albums.Title AS AlbumTitle, artists.Name AS ArtistName, \
                    genres.Name AS Genre, media_types.Name AS MediaType \
            FROM tracks JOIN albums, artists, genres, media_types \
                WHERE albums.AlbumId = tracks.AlbumId \
                    AND albums.ArtistId = artists.ArtistId AND tracks.GenreId = genres.GenreId \
                    AND tracks.MediaTypeId = media_types.MediaTypeId"
    fields = {}

    if id:
        try:
            int(id)
            fields['tracks.TrackID'] = id
        except ValueError:
            return '<h3>Id must be numeric</h3>'
    else:
        return '<h3>Enter track id</h3>'

    query += " AND " + ''.join(f"{key}=?" for key in fields.keys())
    records = execute_query(query=query, args=tuple(fields.values()))
    return my_format_records(records)

@app.route("/total-time")
def get_total_track_time():
    query = 'SELECT SUM(Milliseconds) FROM tracks;'
    records = execute_query(query=query, args=())
    hours = int(records[0][0]) / 3600000
    minutes = int(str(hours).split('.')[1]) * 60

    return f"<h3>Total tracks time: {str(hours).split('.')[0]} hours {str(minutes).split('.')[0][:2]} minutes</h3>"


app.run(port=5001, debug=True)


