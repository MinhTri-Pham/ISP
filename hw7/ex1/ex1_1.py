import csv

EMAIL = 'donald.trump@whitehouse.gov'
PUBLIC_DB = 'anon_data/imdb-1.csv' 
ANON_DB = 'anon_data/com402-1.csv'

# Store all rows in public DB
# Also store DT's rows in public DB
public_dt_rows = []
public_rows = []
with open(PUBLIC_DB, 'r') as public_db_file:
    public_db_reader = csv.reader(public_db_file)
    for public_row in public_db_reader:
        if (public_row[0] == EMAIL):
            public_dt_rows.append(public_row)
        public_rows.append(public_row)    

# Find hash to movie name mappings
# Find hash of DT's email
anon_rows = []
dt_hash = ""
movie_hash_map = dict()
with open(ANON_DB, 'r') as anon_db_file:
    anon_db_reader = csv.reader(anon_db_file)
    found_dt_hash = False
    for anon_row in anon_db_reader:
        if not found_dt_hash:
            # Check if this row (in anonymised DB) corresponds to a DT's row in the public DB by comparing date and rating
            for public_dt_row in public_dt_rows:
                if anon_row[2] == public_dt_row[2] and anon_row[3] == public_dt_row[3]:
                    dt_hash = anon_row[0]
                    found_dt_hash = True
                    break
        # If we have an entry in the public DB with the same date and the same rating, we probably found hash to movie name mapping         
        movie_hash = anon_row[1]
        if movie_hash not in movie_hash_map:
            for public_row in public_rows:
                if anon_row[2] == public_row[2] and anon_row[3] == public_row[3]:
                    movie_hash_map[movie_hash] = public_row[1]
                    break
        anon_rows.append(anon_row) 


# Now find movie DT has rated in anonymised DB
for anon_row in anon_rows:
    if anon_row[0] == dt_hash:
        print(movie_hash_map[anon_row[1]])