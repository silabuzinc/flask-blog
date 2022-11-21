import unittest
from app.models.usuarios import AnonymousUser, User
from app.models.posts import Post
from app.models.roles import Role
from main import app
from app import create_app
from app.db import db
from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from base64 import b64encode
import json
class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app_context = app.app_context()
    
        self.app_context.push()
        self.client = app.test_client(use_cookies=True)

    def get_api_headers(self, username, password):
        return {
            'Authorization':
            'Basic ' + b64encode(
            (username + ':' + password).encode('utf-8')).decode('utf-8'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    def test_post(self):
        r = Role.query.filter_by(name='User').first()
        self.assertIsNotNone(r)
        u = User(username = "marc", email='marc@example.com', role=r)
        u.set_password("password")
        self.assertIsNotNone(u)
        db.session.add(u)
        db.session.commit()
        response = self.client.post(
                '/postJson/',
        headers=self.get_api_headers('john@example.com', 'password'),
        data=json.dumps({'body': 'body of the *blog* post'}))

        self.assertEqual(response.status_code, 201)

if __name__ ==  " __main__":
      unittest.main()