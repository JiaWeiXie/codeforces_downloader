from codeforces_downloader import __version__
from codeforces_downloader.downloader import get_submit_source_data


def test_version():
    assert __version__ == '0.1.0'


def test_downloader():
    submission_url = "https://codeforces.com/problemset/submission/1687/159699643"
    submit_source_url = "https://codeforces.com/data/submitSource"
    json_data = get_submit_source_data(submission_url, submit_source_url)
    assert json_data
