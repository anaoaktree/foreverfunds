"""
Definition of the database schema
"""

import datetime as dt
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


# User class for db
class User(db.Model):
    """
    Table with all user
    """
    __tablename__ = 'user'
    username = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(128))
    email = db.Column(db.String(70))
    insert_date = db.Column(db.TIMESTAMP)
    last_modified = db.Column(db.TIMESTAMP)
    permission = db.Column(db.Integer)

    def __init__(self, username, password, email, permission=0):  # TODO: create permissions mapping
        self.username = username
        self.password = password
        self.email = email
        self.insert_date = dt.datetime.today()
        self.last_modified = dt.datetime.today()
        self.permission = permission

    def setPassword(self, password):
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username


