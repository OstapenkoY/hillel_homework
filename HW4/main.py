import sqlite3
from datetime import timedelta

from flask import Flask
from webargs import fields
from webargs.flaskparser import use_kwargs

from utils import format_records, track_info_format_records


def execute_query(query, args=()):
    with sqlite3.connect('chinook.db') as connection:
        cursor = connection.cursor()
        cursor.execute(query, args)
        connection.commit()
        records = cursor.fetchall()
    return records


app = Flask(__name__)


@app.route("/order-price")
@use_kwargs(
    {
        "country": fields.Str(required=False,
                              load_default=None)
    },
    location="query"
)
def order_price(country):
    query = """SELECT invoices.BillingCountry, round(sum(invoice_items.UnitPrice), 2)
               FROM invoice_items 
               JOIN invoices ON invoice_items.InvoiceId = invoices.InvoiceId"""
    if country:
        query += f" AND invoices.BillingCountry='{country}' GROUP BY invoices.BillingCountry;"
    else:
        query += " GROUP BY invoices.BillingCountry;"
    records = execute_query(query)
    return format_records(records)


@app.route("/track-info")
@use_kwargs(
    {
        "id": fields.Int(required=False,
                         load_default=None)
    },
    location="query"
)
def get_all_info_about_track(id):
    query = """SELECT tracks.TrackID, tracks.Composer, tracks.Name AS TrackName, tracks.UnitPrice, 
               tracks.Milliseconds, tracks.Bytes, albums.Title AS AlbumTitle, artists.Name AS ArtistName, 
               genres.Name AS Genre, media_types.Name AS MediaType 
               FROM tracks JOIN albums, artists, genres, media_types 
               WHERE albums.AlbumId = tracks.AlbumId 
               AND albums.ArtistId = artists.ArtistId AND tracks.GenreId = genres.GenreId 
               AND tracks.MediaTypeId = media_types.MediaTypeId"""
    query += " AND " + f"tracks.TrackID='{id}'"
    records = execute_query(query=query)
    return track_info_format_records(records)


@app.route("/total-time")
def get_total_track_time():
    query = 'SELECT SUM(Milliseconds) FROM tracks;'
    records = execute_query(query=query, args=())
    hours = int(records[0][0]) / 3600000
    minutes = int(str(hours).split('.')[1]) * 60

    return f"<h3>Total tracks time: {str(hours).split('.')[0]} hours {str(minutes).split('.')[0][:2]} minutes</h3>"


app.run(port=5001, debug=True)


