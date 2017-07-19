"""
Simple configuration file. It also checks if you have any local settings defined, in which case it overrides the default values
"""
import os

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') # for heroku. Add your own in your local_settings.py
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_POOL_RECYCLE = 299

SECRET_KEY = os.urandom(24) ## TODO: Set a better secret

# GITHUB SETTINGS

GITHUB_USER= os.environ.get("GITHUB_USER")
GITHUB_PASSWORD = os.environ.get("GITHUB_PASSWORD")

# Token needed to download files - see here on how to get it https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/
GITHUB_TOKEN = 'EXamP3'

GITHUB_FUNDS_FOLDER = 'https://github.com/chassang/funds_example/tree/master/db/funds'



# For GitHub Enterprise
# 'GITHUB_BASE_URL' = 'https://HOSTNAME/api/v3/'
# 'GITHUB_AUTH_URL' = 'https://HOSTNAME/login/oauth/'


# MAIL SETTINGS

MAIL_SERVER = os.environ.get("MAIL_SERVER")
MAIL_PORT = os.environ.get("MAIL_PORT")
MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS")
MAIL_USE_SSL = os.environ.get("MAIL_USE_SSL")
MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER")


try:
   from local_settings import *  # variables in local config will override the values above
except ImportError:
    pass
