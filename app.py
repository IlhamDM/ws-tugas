#6D/18090122/Dimas Ilham M
#6D/18090139?Alfan Nur Rabbani

import os, random, string

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import jsonify
import json
from flask_httpauth import HTTPTokenAuth
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.attributes import QueryableAttribute

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "user.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)
auth = HTTPTokenAuth(scheme='Bearer')


class User(db.Model):
    username = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    password = db.Column(db.String(80), unique=False, nullable=False, primary_key=False)
    token = db.Column(db.String(225), unique=True, nullable=True, primary_key=False)


# tulis command CURL utk request end point ini lengkap dengan data body jsonnya

#username:18090122 password:dimas
#username:18090139 password:alfan
#curl -i -X POST http://localhost:7000/api/v1/login -d "username=,password="

#tapi tidak dapat memakai perintah curl selalu false, tapi bisa menggunakan postman
@app.route("/api/v1/login", methods=["POST"])
def login():
    username = request.values.get('username')
    password = request.values.get('password')

    account = User.query.filter_by(username=username, password=password).first()

    if account:
        token = ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=10))

        User.query.filter_by(username=username, password=password).update({'token': token})
        db.session.commit()

        data = {'token': token}
        return jsonify(data)
    else:
        data = {'result': 'false'}
        return jsonify(data)

# tulis command line CURL utk request end point ini lengkap dengan data body jsonnya
#curl -i -X POST http://localhost:7000/api/v2/users/info -d "token hasil curl sebelumnya"
@app.route("/api/v2/users/info", methods=["POST"])
def info():
    token = request.values.get('token')
    account = User.query.filter_by(token=token).first()
    data = {'username': account.username}
    return jsonify(data)



if __name__ == '__main__':
    app.run(host='localhost', debug=True, port=7000)
