from itertools import product
from hashlib import sha256

def read_file(filename):
    with open(filename, encoding='utf-8') as f:
        digests = f.readlines()
    return [x.strip() for x in digests]

def brute_force(chars, minLen, maxLen, digests):
    cracked = {}
    num_cracked = 0
    j = 0
    n = len(digests)
    for length in range(minLen, maxLen + 1):
        for psw in (''.join(i) for i in product(chars, repeat = length)):    
            if j % 300000000 == 0:
                print(j)
            sha = compute_hash(psw)
            if sha in digests:
                cracked[sha] = psw
                print('Found {psw} with hash {sha}'.format(psw=psw, sha=sha))
                num_cracked += 1
                if num_cracked == n:
                    print('Cracked all digests')
                    return cracked
            j += 1        
    return cracked

def compute_hash(password): 
    h = sha256()
    h.update(password.encode())
    return h.hexdigest()    

if __name__ == "__main__":
    digests = read_file('digests_a.txt')  
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
    minLen = 4
    maxLen = 6
    cracked = brute_force(chars, minLen, maxLen, digests)

    with open('passwords_a.txt', 'w') as f:
        for key in cracked:
            f.write("{hash}: {password}\n".format(hash=key, password=cracked[key]))