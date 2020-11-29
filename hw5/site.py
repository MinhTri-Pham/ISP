#!/usr/bin/env python3
import sys
import populate
from flask import Flask
from flask import request, jsonify
import pymysql


app = Flask(__name__)
username = "root"
password = "root"
database = "hw5_ex2"

# This method returns a list of messages in a json format such as
# [
# { "name": <name>, "message": <message> },
# { "name": <name>, "message": <message> },
# ...
# ]
# If this is a POST request and there is a parameter "name" given, then only
# messages of the given name should be returned.
# If the POST parameter is invalid, then the response code must be 500.


@app.route("/messages", methods=["GET", "POST"])
def messages():
    with db.cursor() as cursor:
        if request.method == "GET":
            query = "SELECT DISTINCT name, message FROM messages"
            cursor.execute(query)
            results = cursor.fetchall()
            json = [{"name": result[0], "message": result[1]} for result in results]
            return jsonify(json), 200
        else:
            name = request.form.get('name')
            if not name:
                return "Invalid input", 500
            query = "SELECT DISTINCT name, message FROM messages WHERE name = %s"
            cursor.execute(query,name)
            results = cursor.fetchall()
            json = [{"name": result[0], "message": result[1]} for result in results]
            return jsonify(json), 200


# This method returns the list of users in a json format such as
# { "users": [ <user1>, <user2>, ... ] }
# This methods should limit the number of users if a GET URL parameter is given
# named limit. For example, /users?limit=4 should only return the first four
# users.
# If the paramer given is invalid, then the response code must be 500.
@app.route("/users", methods=["GET"])
def contact():
    with db.cursor() as cursor:
        query = "SELECT DISTINCT name FROM users"
        cursor.execute(query)
        results = cursor.fetchall()
        all_users = [result[0] for result in results]
        limit = request.args.get('limit')
        # No limit parameter given, so display all users
        if not limit:
            return jsonify({"users": all_users}), 200
        try:
            limit = int(limit)
            if limit < 0:
                return "Invalid input", 500
            limited_users = all_users[:limit] 
            return jsonify({"users": limited_users}), 200
        # The limit parameter given is not an int or > number of users, so response code is 500    
        except (ValueError, IndexError):
            return "Invalid input", 500

if __name__ == "__main__":
    db = pymysql.connect("localhost",
                         username,
                         password,
                         database)
    with db.cursor() as cursor:
        populate.populate_db(cursor)
        db.commit()
    print("[+] database populated")

    app.run(host='0.0.0.0', port=80)