from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from services import funds as funds_service
from os import environ
from werkzeug.contrib.cache import SimpleCache
from db.entities import db, User
from login.login_controller import login_manager, validate_login, LoginUser
from flask_login import login_user, login_required, logout_user, current_user


cache = SimpleCache()


app = Flask(__name__,template_folder="templates", static_folder="static")
app.config.from_object('settings')


db.init_app(app)
db.app = app
db.create_all()
login_manager.init_app(app)


# todo: remove this later
admin = User('admin', 'password', 1)
investor = User('investor', 'password', 0)
db.session.add(admin)
db.session.add(investor)
db.session.commit()


# Login callback definitions
@login_manager.user_loader
def user_loader(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return
    log_user = LoginUser()
    log_user.id = username
    log_user.permission = user.permission
    return log_user


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = User.query.filter_by(username=username).first()
    if user is None:
        return
    log_user = LoginUser()
    log_user.id = username
    log_user.permission = user.permission
    # this doesn't seem to be needed but I must check later
    # log_user.is_authenticated = validate_login(user, request.form['password'])

    return log_user



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
        user = User.query.filter_by(username=request.form['username']).first()
        if user is None:
            return render_template('login.html', error="Given username doesn't exist!")
        elif validate_login(user, request.form['password']):

            log_user = LoginUser()
            log_user.id = user.username
            log_user.permission = user.permission
            login_user(log_user)
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error="Username/Password combination doesn't match!")


## Investor private area
@app.route('/home')
@login_required
def home():
    return render_template('investor/home.html')

## Funds routes

@app.route('/funds')
@login_required
def funds():
    return render_template('investor/funds.html', funds = cache.get('funds'))


@app.route('/research')
@login_required
def research():
    return render_template('investor/research.html')
## end investor area

## TODO: add admin to control funds and research

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('landingA'))


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