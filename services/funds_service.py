
from github import Github
from bokeh.embed import components
from bokeh.resources import INLINE
import pandas as pd
import numpy as np
from bokeh.plotting import figure
import base64

from bokeh.models import ColumnDataSource
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn
from bokeh.embed import components
from bokeh.layouts import widgetbox
from datetime import date
from random import randint

import sys
if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO

def get_fund_dict(fund, repo):
    """

    :param fund: Fund ContentFile from the Github call
    :param g_token: Github token to download files
    :return: dictionary with the relevant fund fields for analysis
    """
    allocation_file_url, allocation_data, value_data, assets_file_url = '', '', '', ''
    for file in fund.raw_data:
        download_url= file.get('download_url', '')
        # download_url, _ = file.get('download_url', '').split('?') ## TODO: figure out how token works here
        # download_url+='?token={g_token}'.format(g_token=g_token)
        if file.get('name') == 'allocation.csv':
            allocation_file_url = download_url
            allocation_file_content = repo.get_contents('%s/allocation.csv' % fund.path)
            allocation_data = base64.b64decode(allocation_file_content.content)

        elif file.get('name') == 'value.csv':
            assets_file_url = download_url
            value_file_content = repo.get_contents('%s/value.csv' % fund.path)
            value_data = base64.b64decode(value_file_content.content)



    return {
        "name": fund.name,
        "path_in_repo": fund.path,
        "allocation_file_url": allocation_file_url,
        "allocation_file_content": allocation_data,
        "value_file_content": value_data,
        "assets_file_url": assets_file_url,
        "last_modified": fund.last_modified
    }

def get_latest_funds(user, passwd):
    github = Github(user, passwd)
    for repo in github.get_user().get_repos():
        if repo.name == 'funds_example':
            return list(map(lambda fund: get_fund_dict(fund, repo), repo.get_contents('db/funds')))
    return []


def get_allocation_table(fund):

    allocation_data = pd.read_csv(StringIO(fund.get('allocation_file_content')))

    data = {col: allocation_data[col] for col in allocation_data.columns}

    source = ColumnDataSource(data)

    columns = [
        TableColumn(field=col, title=col) for col in allocation_data.columns
    ]
    data_table = DataTable(source=source, columns=columns, sizing_mode='scale_width', height=400)

    script, alloc_data = components(widgetbox(data_table, sizing_mode='scale_width'))
    return script, alloc_data

def get_performance_graph(fund):
    # prepare some data
    # data = requests.get(fund.get('assets_file_url'))
    values_data = pd.read_csv(StringIO(fund.get('value_file_content')), names=['date', 'value'], skiprows=0)

    # create a new plot with a a datetime axis type
    p = figure(width=800, height=350, x_axis_type="datetime")

    # add renderers
    p.line(pd.to_datetime(values_data['date'][1:]), pd.to_numeric(values_data['value'][1:]), line_width=2, color='navy', alpha=0.8, legend='value')

    # NEW: customize by setting attributes
    p.title.text = "Fund {{fund}} performance".format(fund=fund)
    p.legend.location = "top_left"
    # p.grid.grid_line_alpha = 0
    p.xaxis.axis_label = 'Date'
    # p.yaxis.axis_label = 'Price'
    # p.ygrid.band_fill_color = "olive"
    # p.ygrid.band_fill_alpha = 0.1

    script, html_component = components(p)

    plot_resources =''.join(INLINE.js_raw + INLINE.css_raw+ INLINE.js_files+INLINE.css_files)+ script

    return script, html_component