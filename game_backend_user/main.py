import os
import json
import uuid
from flask import request

from flask_sqlalchemy import SQLAlchemy
from flask import Flask

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

#TODO use PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# data class
class User(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(250), unique=False, nullable=False)
    age = db.Column(db.Integer(), nullable=False)

    def __init__(self, id, name, age):
        self.id = id
        self.name = name
        self.age = age

    def toDict(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age
            }

with app.app_context():
    db.create_all()



#home
@app.route("/")
def home():
    return 'Welcome to here and now!'


#get all users
@app.route("/users", methods=["GET"])
def allUsers():
    users = db.session.query(User).all()
    response = [user.toDict() for user in users]
    return json.dumps(response)


#get user with id
@app.route("/users/<id>", methods=["GET"])
def get_user(id):

    user = User.query.get(id)
    return json.dumps(user.toDict())

#add user
@app.route("/users", methods=["POST"])
def add():
    content = request.json

    new_user = User(
        id= str(uuid.uuid4()),
        name=content["name"],
        age=content["age"]
    )

    db.session.add(new_user)
    db.session.commit()

    return json.dumps(new_user.toDict())


#delete user with id
@app.route("/users/<id>", methods=["DELETE"])
def delete_user(id):

    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return json.dumps(user.toDict())

#update user with id
@app.route("/users/<id>", methods=["PUT"])
def update(id):
    userToUpdate = User.query.get(id)
    userToUpdate.age = request.json["age"]

    db.session.commit()

    return json.dumps(userToUpdate.toDict())


if __name__ == '__main__':
    app.run(debug=True)
