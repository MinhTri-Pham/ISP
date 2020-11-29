import csv

EMAIL = 'donald.trump@whitehouse.gov'
PUBLIC_DB = 'anon_data/imdb-1.csv' 
ANON_DB = 'anon_data/com402-1.csv'

public_dt_rows = []

with open(PUBLIC_DB, 'r') as public_db_file:
    public_db_reader = csv.reader(public_db_file)
    for public_row in public_db_reader:
        if (public_row[0] == EMAIL):
            public_dt_rows.append(public_row)

with open(ANON_DB, 'r') as anon_db_file:
    anon_db_reader = csv.reader(anon_db_file)
    for anon_row in anon_db_reader:
        for public_dt_row in public_dt_rows:
            if (anon_row[2] == public_dt_row[2] and anon_row[3] == public_dt_row[3]):
                print(public_dt_row[1])
