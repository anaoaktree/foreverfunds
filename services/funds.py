
from github import Github
import json


def get_fund_dict(fund):
    """

    :param fund: Fund ContentFile from the Github call
    :return: dictionary with the relevant fund fields for analysis
    """
    allocation_file_url, assets_file_url = '', ''
    for file in fund.raw_data:
        download_url = file.get('download_url', '')
        if file.get('name') == 'allocation.csv':
            allocation_file_url = download_url
        elif file.get('name') == 'assets.csv':
            assets_file_url = download_url

    return {
        "name": fund.name,
        "path_in_repo": fund.path,
        "allocation_file_url": allocation_file_url,
        "assets_file_url": assets_file_url,
        "last_modified": fund.last_modified
    }

def get_latest_funds(user, passwd):
    github = Github(user, passwd)
    for repo in github.get_user().get_repos():
        if repo.name == 'funds_example':
            return list(map(get_fund_dict, repo.get_contents('db/funds')))
    return []