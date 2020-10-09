import csv
import sqlite3


conn = sqlite3.connect('db.sqlite3')
cur = conn.cursor()

with open('dummy_data.csv', 'r') as f:
    reader = csv.DictReader(f)
    for line in reader:
        if line['type'] == 'Movie':
            is_movie = True
        else:
            is_movie = False
        row = [line['show_id'], is_movie, line['title'],
               line['director'], line['release_year'],
               line['rating'], line['duration'], line['description']]
        cur.execute("INSERT INTO flix_show VALUES (null, ?, ?, ?, ?, ?, ?, ?, ?);", row)
conn.commit()
