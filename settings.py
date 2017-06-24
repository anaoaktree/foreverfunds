"""
Simple configuration file. It also checks if you have any local settings defined, in which case it overrides the default values
"""
import os

SQLALCHEMY_DATABASE_URI = 'mysql://root:1234@localhost/foreverfunds'
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_POOL_RECYCLE = 299

SECRET_KEY = os.urandom(24) ## TODO: Set a better secret

try:
   from local_config import *  # variables in local config will override the values above
except ImportError:
    pass
