"""
Simple configuration file. It also checks if you have any local settings defined, in which case it overrides the default values
"""
import os

SQLALCHEMY_DATABASE_URI = 'sqlite://' # 'mysql://root:1234@localhost/foreverfunds'
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_POOL_RECYCLE = 299

SECRET_KEY = os.urandom(24) ## TODO: Set a better secret

# GITHUB SETTINGS

GITHUB_USER= os.environ.get("GITHUB_USER")
GITHUB_PASSWORD = os.environ.get("GITHUB_PASSWORD")

GITHUB_FUNDS_FOLDER = 'https://github.com/chassang/funds_example/tree/master/db/funds'



# For GitHub Enterprise
# 'GITHUB_BASE_URL' = 'https://HOSTNAME/api/v3/'
# 'GITHUB_AUTH_URL' = 'https://HOSTNAME/login/oauth/'




try:
   from local_settings import *  # variables in local config will override the values above
except ImportError:
    pass
