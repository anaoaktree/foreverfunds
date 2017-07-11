

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from services import funds as funds_service
from os import environ
from werkzeug.contrib.cache import SimpleCache

cache = SimpleCache()

# from db.entities import db


app = Flask(__name__,template_folder="templates", static_folder="static")
app.config.from_object('settings')

# db.init_app(app) uncomment when db entites are functioning


# Endpoint definition
@app.route('/')
def landingA():
    return render_template('landingA.html')

@app.route('/about')
def landingB():
    return render_template('landingB.html')


@app.route('/login', methods=['GET', 'POST'])
def dummy_login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        session['username'] = request.form['username']
        return redirect(url_for('home'))

## Investor private area
## TODO: add login required decorator
@app.route('/home')
def home():
    return render_template('investor/home.html')




## Funds routes

@app.route('/funds')
def funds():
    return render_template('investor/funds.html', funds = cache.get('funds'))


@app.route('/research')
def research():
    return render_template('investor/research.html')
## end investor area

## TODO: add admin to control funds and research

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.before_first_request
def update_funds():
    """
    Gets the latest funds before the first request executes
    :return:
    """
    print(app.config.get('GITHUB_USER'))
    print(app.config.get('GITHUB_PASSWORD'))

    g_user, g_pass = app.config.get('GITHUB_USER'), app.config.get('GITHUB_PASSWORD')
    cache.set('funds', funds_service.get_latest_funds(g_user, g_pass))
    if not cache.get('funds'):
        session['messages']='User has no access to funds repo so no funds are available'


if __name__ == "__main__":
    app.run()