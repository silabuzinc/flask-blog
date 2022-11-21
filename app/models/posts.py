from app.db import db
from datetime import datetime
from flask import url_for
from wtforms import ValidationError

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def to_json(self):
        json_post = {
            'post_id': self.id,
            'body': self.body,
            'timestamp': self.timestamp,

        }
        return json_post
    # ...
    def from_json(json_post):
        body = json_post.get('body')
        if body is None or body == '':
            raise ValidationError('El post no tiene cuerpo')
        return Post(body = body)
