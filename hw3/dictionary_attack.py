from hashlib import sha256
from itertools import product

def read_file(filename):
    with open(filename, encoding='utf-8') as f:
        digests = f.readlines()
    return [x.strip() for x in digests]


def substitute_for_letters(word, substitutions):
    options = ((c,) if c not in substitutions else (c, str(substitutions[c])) for c in word)
    return (''.join(o) for o in product(*options))

def dictionary_attack(passwords, digests, substitutions):
    n = len(digests)
    cracked = {}
    
    for password in passwords:
        
        if len(password) > 15:
            continue

        variations = substitute_for_letters(password, substitutions)    
        for variation in variations:
            sha = compute_hash(variation)
            if sha in digests:
                cracked[sha] = variation
                print('Found {psw} with hash {sha}'.format(psw=variation, sha=sha))
                if len(cracked) == n:
                    print('Cracked all digests')
                    return cracked

            titled_variation = variation.title()
            if variation != titled_variation:
                sha_title = compute_hash(titled_variation)
                if sha_title in digests:
                    cracked[sha_title] = titled_variation
                    print('Found {psw} with hash {sha}'.format(psw=titled_variation, sha=sha_title))
                    if len(cracked) == n:
                        print('Cracked all digests')
                        return cracked
        
        password_titled = password.title()
        if (password_titled != password):
            variations = substitute_for_letters(password_titled, substitutions)    
            for variation in variations:
                sha = compute_hash(variation)
                if sha in digests:
                    cracked[sha] = variation
                    print('Found {psw} with hash {sha}'.format(psw=variation, sha=sha))
                    if len(cracked) == n:
                        print('Cracked all digests')
                        return cracked

        i += 1            
    return cracked
    
def compute_hash(password): 
    h = sha256()
    h.update(password.encode())
    return h.hexdigest()    

if __name__ == "__main__":
    digests = read_file('digests_b.txt')   
    passwords = read_file('rockyou.txt')  
    substitutions = { 'e': 3, 'o': 0, 'i': 1}
    
    cracked = dictionary_attack(passwords, digests, substitutions)

    with open('passwords_b.txt', 'w') as f:
        for key in cracked:
            f.write("{hash}: {password}\n".format(hash=key, password=cracked[key]))