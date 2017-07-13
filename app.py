

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from services import funds as funds_service
from werkzeug.contrib.cache import SimpleCache

from bokeh.models import ColumnDataSource
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn
from bokeh.embed import components
from datetime import date
from random import randint

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

    data = dict(
        dates=[date(2014, 3, i + 1) for i in range(10)],
        downloads=[randint(0, 100) for i in range(10)],
    )
    source = ColumnDataSource(data)

    columns = [
        TableColumn(field="dates", title="Date", formatter=DateFormatter()),
        TableColumn(field="downloads", title="Downloads"),
    ]
    data_table = DataTable(source=source, columns=columns, width=400, height=280)

    script, alloc_data = components(data_table)

    js_resources = ''#INLINE.render_js()
    css_resources = '' #INLINE.render_css()
    allocation_divs_dict, performance_graph_dict = {}, {}

    extra_resources = []

    for fund in cache.get('funds'):
        allocation_divs_dict[fund.get('name')] = alloc_data
        graph_script, fund_graph_dict = funds_service.get_performance_graph(fund)
        performance_graph_dict[fund.get('name')] = fund_graph_dict
        extra_resources.append(graph_script)




    return render_template('investor/funds.html',
                           funds = cache.get('funds'),
                           allocation_divs = allocation_divs_dict,
                           performance_graphs = performance_graph_dict,
                           js_resources = js_resources,
                           css_resources = css_resources,
                           extra_scripts = ''.join(extra_resources)
                           )


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

    g_user, g_pass, g_token = app.config.get('GITHUB_USER'), app.config.get('GITHUB_PASSWORD'), app.config.get('GITHUB_TOKEN')
    cache.set('funds', funds_service.get_latest_funds(g_user, g_pass, g_token))
    if not cache.get('funds'):
        session['messages']='User has no access to funds repo so no funds are available'


if __name__ == "__main__":
    app.run()