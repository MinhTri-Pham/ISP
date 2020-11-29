import csv
import operator

EMAIL = 'donald.trump@whitehouse.gov'
PUBLIC_DB = 'anon_data/imdb-2.csv' 
ANON_DB = 'anon_data/com402-2.csv'


def sort_dict_by_value(dictionary):
    sorted_tuples = sorted(dictionary.items(), key=operator.itemgetter(1))
    sorted_dict = {k: v for k, v in sorted_tuples}
    return sorted_dict

# Find movie name frequencies in public DB
# Store rows for later
movie_name_counts = dict()
public_rows = []
with open(PUBLIC_DB, 'r') as public_db_file:
    public_db_reader = csv.reader(public_db_file)
    for public_row in public_db_reader:
        movie_name = public_row[1]
        if movie_name in movie_name_counts:
            movie_name_counts[movie_name] += 1
        else:
            movie_name_counts[movie_name] = 1
        public_rows.append(public_row)


# Find movie hash frequencies in anonymised DB
# Store rows for later
movie_hash_counts = dict()
anon_rows = []
with open(ANON_DB, 'r') as anon_db_file:
    anon_db_reader = csv.reader(anon_db_file)
    for anon_row in anon_db_reader:
        movie_hash = anon_row[1]
        if movie_hash in movie_hash_counts:
            movie_hash_counts[movie_hash] += 1
        else:
            movie_hash_counts[movie_hash] = 1   
        anon_rows.append(anon_row)

# Sort both and establish movie hash to movie name mappings          
sorted_movie_name_counts = sort_dict_by_value(movie_name_counts)
sorted_movie_hash_counts = sort_dict_by_value(movie_hash_counts)
sorted_movie_hashes = list(sorted_movie_hash_counts.keys())
sorted_movie_names = list(sorted_movie_name_counts.keys())

movie_hash_map = dict()
num_movies = len(sorted_movie_hashes)
for i in range(num_movies):
    movie_hash_map[sorted_movie_hashes[i]] = sorted_movie_names[i]

# Use mappings to find DT's email hash
found_dt_hash = False
dt_hash = ""
for anon_row in anon_rows:
    if not found_dt_hash:
        for public_row in public_rows:
            if movie_hash_map[anon_row[1]] == public_row[1] and public_row[0] == EMAIL:
                dt_hash = anon_row[0]
                found_dt_hash = True
                break
    else:
        break

# Now find movie DT has rated in anonymised DB
for anon_row in anon_rows:
    if anon_row[0] == dt_hash:
        print(movie_hash_map[anon_row[1]])