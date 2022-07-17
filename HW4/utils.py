def format_records(records: list) -> str:
    return '<br>'.join(str(record) for record in records)


def track_info_format_records(records: list) -> str:
    title_names = ['TrackId', 'Composer', 'TrackName', 'UnitPrice',
                   'Milliseconds', 'Bytes', 'AlbumTitle',
                   'ArtistName', 'Genre', 'MediaType']
    total = list(zip(title_names, records[0]))
    return '<br>'.join(str(record) for record in total)



