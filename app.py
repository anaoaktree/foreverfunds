

from flask import Flask, render_template, request, redirect, url_for, session, abort
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


@app.route('/funds')
def funds():
    return render_template('investor/funds.html')


@app.route('/research')
def research():
    return render_template('investor/research.html')
## end investor area

## TODO: add admin to control funds and research

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run()