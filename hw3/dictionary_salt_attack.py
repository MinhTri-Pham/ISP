from hashlib import sha256

def read_file(filename):
    with open(filename, encoding='utf-8') as f:
        digests = f.readlines()
    return [x.strip() for x in digests]


def dictionary_salt_attack(passwords, digest_salt_dict):
    cracked = {}    
    for password in passwords:
        for digest, salt in digest_salt_dict.items():
            hash_psw_salt = compute_hash(password,salt)
            if hash_psw_salt == digest:
                print('Found {psw} with hash {hash} and salt {salt}'.format(psw=password, hash=hash_psw_salt, salt = salt))
                digest_salt = '{hash} ({salt})'.format(hash = hash_psw_salt, salt = salt)
                cracked[digest_salt] = password
                if num_cracked == len(digest_salt_dict):
                    print('Cracked all digests')
                    return cracked

def compute_hash(password, salt): 
    h = sha256()
    h.update(password.encode())
    h.update(salt.encode())
    return h.hexdigest()    

if __name__ == "__main__":
    digests_salts = read_file('digests_c.txt')   
    passwords = read_file('rockyou.txt')  

    digest_salt_dict = {}    
    for digest_salt in digests_salts:
        line = digest_salt.split()
        digest = line[0]
        salt = line[1][1:3]
        digest_salt_dict[digest] = salt

    cracked = dictionary_salt_attack(passwords, digest_salt_dict)

    with open('passwords_c.txt', 'w') as f:
        for key in cracked:
            f.write("{hash}: {password}\n".format(hash=key, password=cracked[key]))