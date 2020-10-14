import hmac
import os
from collections import defaultdict
from time import time
from base64 import b64encode, b64decode
from flask import Flask, request, make_response

app = Flask(__name__)

cookie_name = "LoginCookie"

def new_random(): return os.urandom(20)


secret_dict = defaultdict(new_random)


def compute_hmac(username, timestamp, user_type):

    user_secret = secret_dict[username]
    return hmac.new(user_secret, bytes(username + str(timestamp) + user_type, 'utf-8')).hexdigest().upper()

@app.route("/login",methods=['POST'])
def login():
    # Get username and password from POST request
    username = request.form['username']
    password = request.form['password']

    # Check if username and password exist
    if (not username) | (not password):
        return 'Invalid login data', 401

    # Make cookie
    cookie = ""
    timestamp = round(time()) 

    if (username == 'admin' and password == '42'):
        user_type = 'admin'
        cookie = '{},{},com402,hw2,ex2,admin,{}'.format(username, timestamp, compute_hmac(username, timestamp, user_type))
    else:
        user_type = 'user'
        cookie = '{},{},com402,hw2,ex2,user,{}'.format(username, timestamp, compute_hmac(username, timestamp, user_type))

    
    # Convert cookie to byte-like object and encode in base64
    cookie = b64encode(bytes(cookie, 'utf-8'))

    # Make response and attach the cookie
    response = make_response('Welcome {}!'.format(username))
    response.set_cookie(cookie_name, cookie)

    return response


@app.route("/auth",methods=['GET'])
def auth():
    cookie = request.cookies.get(cookie_name)
    if not cookie:
        return 'No cookie is present, 403'
    
    cookie = b64decode(cookie).decode('utf-8')
    cookie_components = cookie.split()

    # Check that the structure is right
    if len(cookie_components) != 7:
        return 'Cookie has been tampered with, 403'


    # Check HMAC is right
    username = cookie_components[0]
    timestamp = cookie_components[1]
    user_type = cookie_components[5]    
    hmac_ = cookie_components[6]
    if not hmac.compare_digest(hmac_, compute_hmac(username, timestamp, user_type)):
        return 'Cookie has been tampered with, 403'

    if user_type == 'user':
        return 'Have a simple user, 201'
    elif user_type == 'admin':
        return 'Have a simple user, 200'   
    return 'Cookie has been tampered with, 403'   

if __name__ == '__main__':
    app.run()