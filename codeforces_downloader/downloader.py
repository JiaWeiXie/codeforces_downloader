from typing import Any, Dict, List, Union
from urllib.parse import urlparse

import requests
from pyquery import PyQuery as pq

__all__ = [
    "get_submit_source_data",
]


def get_web(client: requests.Session, url: str) -> str:
    r = client.get(url)
    r.raise_for_status()
    return r.text


def parse_html(context: str) -> str:
    dom = pq(context)
    form = dom.find("#pageContent > div.add-submission-to-problem-solutions-box > form")
    csrf_token = form("input").text()
    return csrf_token


def get_submit_source(
    client: requests.Session,
    url: str,
    submission_id: str,
    csrf_token: str,
):
    payload = {
        "submissionId": submission_id,
        "csrf_token": csrf_token,
    }
    r = client.post(url, data=payload)
    r.raise_for_status()
    return r.json()


def format_json(
    json_data: Dict[str, Union[str, Any]]
) -> List[Dict[str, Union[str, Any]]]:
    format_data = []
    test_count = int(json_data.get("testCount", "0"))
    for idx in range(1, test_count + 1):
        format_data.append(
            dict(
                time_consumed=json_data.get(f"timeConsumed#{idx}"),
                memory_consumed=json_data.get(f"memoryConsumed#{idx}"),
                verdict=json_data.get(f"verdict#{idx}"),
                accepted=json_data.get(f"accepted#{idx}"),
                rejected=json_data.get(f"rejected#{idx}"),
                inputs=json_data.get(f"input#{idx}"),
                outputs=json_data.get(f"output#{idx}"),
                answer=json_data.get(f"answer#{idx}"),
                exit_code=json_data.get(f"exitCode#{idx}"),
                checker_stdout_and_stderr=json_data.get(
                    f"checkerStdoutAndStderr#{idx}"
                ),
                checker_exit_code=json_data.get(f"checkerExitCode#{idx}"),
                diagnostics=json_data.get(f"diagnostics#{idx}"),
            )
        )

    return format_data


def get_submit_source_data(submission_url: str, submit_source_url: str):
    submission_id = list(
        filter(
            bool,
            urlparse(submission_url).path.split("/"),
        ),
    )[-1]
    with requests.Session() as client:
        html = get_web(client, submission_url)
        csrf_token_ = parse_html(html)
        json_data = get_submit_source(
            client,
            submit_source_url,
            submission_id,
            csrf_token_,
        )
        return format_json(json_data)


if __name__ == "__main__":
    import json

    def run():
        submission_url = "https://codeforces.com/problemset/submission/1687/159699643"
        submit_source_url = "https://codeforces.com/data/submitSource"
        json_data = get_submit_source_data(submission_url, submit_source_url)
        with open("test_submit_source_format.json", "w") as f:
            json.dump(json_data, f)
        print(json_data)

    run()
