from codeforces_downloader import __version__
from codeforces_downloader.downloader import get_all_testcase


def test_version():
    assert __version__ == "0.2.0"


def test_downloader():
    submission_url = "https://codeforces.com/problemset/submission/1687/159699643"
    json_data = get_all_testcase(submission_url)
    assert json_data
