def format_records(records: list) -> str:
    return '<br>'.join(str(record) for record in records)


def my_format_records(records: list) -> str:
    title_names = ['TrackId', 'Composer', 'TrackName', 'UnitPrice',
                   'Milliseconds', 'Bytes', 'AlbumTitle',
                   'ArtistName', 'Genre', 'MediaType']
    d = {}
    for i in range(10):
        d[title_names[i]] = records[0][i]
    return str({f'<br>{k}: {v}' for k, v in d.items()})


