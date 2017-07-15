## LOCAL config

create a local_settings.py file (is ignored by git) and add your github credentials like:

GITHUB_USER= 'XXX'
GITHUB_PASSWORD = 'YYY'

you must also add the following credentials to send an email:

MAIL_SERVER = 'XXX'
MAIL_PORT = n
MAIL_USE_TLS = True|False
MAIL_USE_SSL = True|False
MAIL_USERNAME = 'mail@example.com'
MAIL_PASSWORD = 'YYY'
MAIL_DEFAULT_SENDER = 'mail@example.com'





### Templates

Contains the template structure for the website. All templates inherit the base template.

### Road map
- Setup rendering of funds page and research page according to git file
- add circle CI for testing before pushing and automatic deployment to heroku
-