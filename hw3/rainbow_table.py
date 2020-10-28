from hashlib import sha256

LENGTH = 8
BASE = 36
CHARSET = 'abcdefghijklmnopqrstuvwxyz0123456789'
NUM_REDUCTION_FUNCTIONS = 10000

def read_file(filename):
    with open(filename, encoding='utf-8') as f:
        digests = f.readlines()
    return [x.strip() for x in digests]

def reduction_function(h, index):
    # Convert hash h to integer h_int and reduce to specified LENGTH
    # By converting h_int + index to given BASE with given CHARSET, one character at a time until we reach desired LENGTH 
    h_int = int(h, 16) + index
    result = ''
    for i in range(LENGTH):
        result += CHARSET[h_int % BASE]
        h_int = h_int // BASE   
    return result

def init_reduction_function(h_int):
    # Equivalent to reduction function with index 0
    result = ''
    for i in range(LENGTH):
        result += CHARSET[h_int % BASE]
        h_int = h_int // BASE   
    return result    

def hash_function(psw):
    h = sha256()
    h.update(psw.encode())
    return h.hexdigest()  

def hash_and_reduce(psw, index):
    result = hash_function(psw)
    return reduction_function(result, index)

def reduce_and_hash(h, index):
    result = reduction_function(h, index)
    return hash_function(result)

def build_rainbow_table():
    num_rows = 10000000 # 10M rows
    num_cols = NUM_REDUCTION_FUNCTIONS # 10k columns
    rainbow_table = {}
    # Use R_0 of row number as starting password
    for row in range(1, num_rows+1):
        start = init_reduction_function(row)
        entry = start
        # Apply H and R_i for i = 1, ..., num_cols
        for col in range(1, num_cols+1):
            entry = hash_function(entry)
            entry = reduction_function(entry, col)
        rainbow_table[entry] = start # Store start and ending points (key is end to look up start when we get a match)    
    return rainbow_table    

def crack_digest(digest, rainbow_table):
    for i in range(NUM_REDUCTION_FUNCTIONS, 0, -1):
        result = reduction_function(digest, i)
        if result in rainbow_table.keys():
            start = rainbow_table[result]
            foundPassword = find_password(digest,start)
            if foundPassword:
                return foundPassword        
        for j in range(i+1, NUM_REDUCTION_FUNCTIONS+1):
            result = hash_and_reduce(result)
            if result in rainbow_table.keys():
                start = rainbow_table[result]
                foundPassword = find_password(digest,start)
                if foundPassword:
                    return foundPassword
    return ''

def find_password(digest, start):
    h = hash_function(start)
    if h == digest:
        return start
    for i in range(1, NUM_REDUCTION_FUNCTIONS):
        temp = reduce_and_hash(h,i)
        if temp == digest:
            return reduction_function(h,i)
        else:
            h = temp        
    return ''        

def rainbow_table_attack(digests):
    rainbow_table = build_rainbow_table()
    cracked = {}
    for digest in digests:
        result = crack_digest(digest, rainbow_table)
        if result:
            cracked[digest] = result
    return cracked


if __name__ == "__main__":
    digests = read_file('digests_d.txt')
    cracked = rainbow_table_attack(digests)
    with open('passwords_a.txt', 'w') as f:
        for key in cracked:
            f.write('{hash}: {password}\n'.format(hash=key, password=cracked[key]))
        f.write('Success rate: {success}'.format(round(100 * (len(cracked) / len(digests)), 1)))    



