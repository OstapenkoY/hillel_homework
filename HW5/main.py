from flask import Flask
import sqlite3
from webargs import validate, fields
from webargs.flaskparser import use_kwargs

app = Flask(__name__)


def execute_query(query):
    with sqlite3.connect('../chinook.db') as connection:
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        records = cursor.fetchall()
    return records


@app.route('/stats_by_city')
@use_kwargs(
    {
        'genre': fields.Str(required=True,
                            validate=validate.Regexp('[a-zA-Z]')
                            )
    },
    location='query'
)
def stats_by_city(genre):
    query = f"""
            SELECT BillingCity, MAX(count) AS Quantity
            FROM
            (SELECT genres.Name, invoices.BillingCity, COUNT(invoices.BillingCity) AS count
            FROM genres
            JOIN tracks ON genres.GenreId = tracks.GenreId
            JOIN invoice_items ON tracks.TrackId = invoice_items.TrackId
            JOIN invoices ON invoices.InvoiceId = invoice_items.InvoiceId
            GROUP BY genres.Name, invoices.BillingCity)
            WHERE Name = '{genre}'
            """
    result = execute_query(query)[0][0]

    return f'<h3>{result}</h3>' if result else '<h3>Incorrect genre</h3>'



if __name__ == '__main__':
    app.run(debug=True)
