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


class Score(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    score = db.Column(db.Integer(), nullable=False)
    user_id = db.Column(db.String(36), nullable=False)

    def __init__(self, id, score, user_id):
        self.id = id
        self.score = score
        self.user_id = user_id

    def to_Dict(self):
        return {
            "id": self.id,
            "score": self.score,
            "user_id": self.user_id
        }


with app.app_context():
    db.create_all()


# get all scores
@app.route("/scores", methods=["GET"])
def allScores():
    scores = db.session.query(Score).order_by(Score.score.desc()).limit(10).all()
    response = [score.to_Dict() for score in scores]
    return json.dumps(response)


# add score
@app.route("/users/<user_id>/scores", methods=["POST"])
def addScore(user_id):
    content = request.json

    new_score = Score(
        id=str(uuid.uuid4()),
        score=content["score"],
        user_id=user_id
    )
    db.session.add(new_score)
    db.session.commit()
    return json.dumps(new_score.to_Dict())


# get user scores
@app.route("/users/<user_id>/scores", methods=["GET"])
def getScore(user_id):

    scores = Score.query.filter_by(user_id=user_id)
    return json.dumps([score.to_Dict() for score in scores])


if __name__ == '__main__':
    app.run(debug=True, port=5001)