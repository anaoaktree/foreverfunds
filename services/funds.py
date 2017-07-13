
from github import Github
from bokeh.embed import components
from bokeh.resources import INLINE
import pandas as pd
import numpy as np
from bokeh.plotting import figure

def get_fund_dict(fund, g_token):
    """

    :param fund: Fund ContentFile from the Github call
    :param g_token: Github token to download files
    :return: dictionary with the relevant fund fields for analysis
    """
    allocation_file_url, assets_file_url = '', ''
    for file in fund.raw_data:
        download_url= file.get('download_url', '')
        # download_url, _ = file.get('download_url', '').split('?') ## TODO: figure out how token works here
        # download_url+='?token={g_token}'.format(g_token=g_token)
        if file.get('name') == 'allocation.csv':
            allocation_file_url = download_url
        elif file.get('name') == 'value.csv':
            assets_file_url = download_url

    return {
        "name": fund.name,
        "path_in_repo": fund.path,
        "allocation_file_url": allocation_file_url,
        "assets_file_url": assets_file_url,
        "last_modified": fund.last_modified
    }

def get_latest_funds(user, passwd, g_token):
    github = Github(user, passwd)
    for repo in github.get_user().get_repos():
        if repo.name == 'funds_example':
            return list(map(lambda fund: get_fund_dict(fund, g_token), repo.get_contents('db/funds')))
    return []


def get_allocation_table():
    pass

def get_performance_graph(fund):
    # prepare some data
    # data = requests.get(fund.get('assets_file_url'))
    values_data = pd.read_csv(fund.get('assets_file_url'), names=['date', 'value'], skiprows=0)
    x = values_data.get('date')[1:]
    y = values_data.get('value')[1:]

    # aapl_dates = np.array(AAPL['date'], dtype=np.datetime64)

    window_size = 30
    window = np.ones(window_size) / float(window_size)
    # aapl_avg = np.convolve(aapl, window, 'same')


    # create a new plot with a a datetime axis type
    p = figure(width=800, height=350, x_axis_type="datetime")

    # add renderers
    # p.circle(aapl_dates, aapl, size=4, color='darkgrey', alpha=0.2, legend='close')
    p.line(x, y, color='navy', legend='avg')

    # NEW: customize by setting attributes
    p.title.text = "AAPL One-Month Average"
    p.legend.location = "top_left"
    p.grid.grid_line_alpha = 0
    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = 'Price'
    p.ygrid.band_fill_color = "olive"
    p.ygrid.band_fill_alpha = 0.1

    script, html_component = components(p)

    plot_resources =''.join(INLINE.js_raw + INLINE.css_raw+ INLINE.js_files+INLINE.css_files)+ script

    return script, html_component