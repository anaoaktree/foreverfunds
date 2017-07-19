
from flask import Flask, render_template, request, redirect, url_for, flash, abort, Session
from flask_login import login_user, login_required, logout_user, current_user
from flask_principal import Principal, Permission, RoleNeed, Identity, identity_changed, identity_loaded, UserNeed
from werkzeug.contrib.cache import SimpleCache
from flask_mail import Mail

from bokeh.resources import INLINE


from db.entities import db, User
from db.user_helper import change_password, validate_password, add_user
from services import funds_service as funds_service
from services.login_service import login_manager, LoginUser
from services.email_service import send_email

cache = SimpleCache()


app = Flask(__name__, template_folder="templates", static_folder="static")
app.config.from_object('config.settings')


db.init_app(app)
db.app = app
db.create_all()
login_manager.init_app(app)
principals = Principal(app)

mail = Mail(app)

admin_permission = Permission(RoleNeed('admin'))

# identity callback definition
@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    # Set the identity user object
    identity.user = current_user

    # Add the UserNeed to the identity
    if hasattr(current_user, 'id'):
        identity.provides.add(UserNeed(current_user.id))

    if hasattr(current_user, 'permission'):
        if current_user.permission == 1:
            identity.provides.add(RoleNeed('admin'))


# Login callback definitions
@login_manager.user_loader
def user_loader(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return
    return LoginUser(username, user.permission)



@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = User.query.filter_by(username=username).first()
    if user is None:
        return
    return LoginUser(username, user.permission)
    # this doesn't seem to be needed but I must check later
    # log_user.is_authenticated = validate_login(user, request.form['password'])


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
            flash("Given username doesn't exist!", 'danger')
            return render_template('login.html')

        elif validate_password(user, request.form['password']):
            log_user = LoginUser(user.username, user.permission)
            login_user(log_user)

            identity_changed.send(app, identity=Identity(current_user.id))
            flash("User successfully logged", 'success')
            return redirect(url_for('home'))
        else:
            flash("Username/Password combination doesn't match!", 'danger')
            return render_template('login.html')


# Investor private area
@app.route('/home')
@login_required
def home():
    return render_template('investor/home.html')


# Funds routes
@app.route('/funds')
@login_required
def funds():

    allocation_divs_dict, performance_graph_dict = {}, {}

    extra_resources = []

    if not cache.get('funds'):
        update_funds()

    for fund in cache.get('funds'):
        alloc_script, alloc_data = funds_service.get_allocation_table(fund)
        allocation_divs_dict[fund.get('name')] = alloc_data

        graph_script, fund_graph_dict = funds_service.get_performance_graph(fund)
        performance_graph_dict[fund.get('name')] = fund_graph_dict

        extra_resources+=([alloc_script, graph_script])


    return render_template('investor/funds.html',
                           funds = cache.get('funds'),
                           allocation_divs = allocation_divs_dict,
                           performance_graphs = performance_graph_dict,
                           js_resources =  INLINE.render_js(),
                           css_resources = INLINE.render_css(),
                           extra_scripts = ''.join(extra_resources)
                           )


@app.route('/research')
@login_required
def research():
    return render_template('investor/research.html')


@app.route('/personal', methods=['GET', 'POST'])
@login_required
def personal():
    if request.method == 'GET':
        return render_template('investor/personal.html')
    if request.form.get('doRegister') is None:
        user = User.query.filter_by(username=current_user.id).first()
        old_password = request.form['old_password']
        new_password1 = request.form['new_password1']
        new_password2 = request.form['new_password2']
        status, message = change_password(user, old_password, new_password1, new_password2)
        if status:
            return redirect(url_for('home'))
        else:
            flash(message, 'danger')
            return render_template('investor/personal.html')
    else:
        if admin_permission.can():
            new_user_name = request.form['username']
            user = User.query.filter_by(username=new_user_name).first()
            if user is None:
                new_user_email = request.form.get('email')
                is_admin = 1 if request.form.get("is_admin") == 1 else 0
                message = send_email(new_user_name, new_user_email, is_admin, mail)
                flash(message, 'success')
                return redirect(url_for('personal'))
            else:
                flash("Given username already exists!", 'danger')
                return render_template('investor/personal.html', error_add_user="Given username already exists!")
        abort(403)


# end investor area
@app.errorhandler(401)
@app.errorhandler(403)
def authorisation_failed(e):
    return render_template('unauthorized.html')


@app.errorhandler(500)
def internal_error(error):
    flash('Something went wrong on our side. Contact admin for more info', 'danger')
    return redirect(url_for('landingA'))


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

    g_user, g_pass = app.config.get('GITHUB_USER'), app.config.get('GITHUB_PASSWORD')
    cache.set('funds', funds_service.get_latest_funds(g_user, g_pass))

    if not cache.get('funds'):
        flash('User has no access to funds repo so no funds are available', 'warning')


if __name__ == "__main__":
    app.run()
