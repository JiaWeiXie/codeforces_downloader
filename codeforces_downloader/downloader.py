from typing import Any, Dict, List
from playwright.sync_api import sync_playwright

__all__ = [
    "get_all_testcase",
]


def get_all_testcase(submission_url: str) -> List[Dict[str, Any]]:
    result = []
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        page = browser.new_page()
        page.goto(submission_url)
        page.click(".click-to-view-tests")
        selector = ".tests-placeholder > .roundbox.borderTopRound"
        js_script = f"() => document.querySelectorAll('{selector}').length > 1"
        page.wait_for_function(js_script)
        elements = page.query_selector_all(selector)
        for element in elements[1:]:
            check_element = element.query_selector(".verdict")
            check_case = check_element.text_content()
            input_element = element.query_selector(".input")
            input_case = input_element.text_content()
            answer_element = element.query_selector(".answer")
            answer_case = answer_element.text_content()
            check = check_case.lower() == "ok"
            if check:
                result.append(
                    dict(
                        verdict=check,
                        inputs=input_case,
                        answer=answer_case,
                    )
                )
        browser.close()
    return result


if __name__ == "__main__":
    import json

    def run():
        submission_url = "https://codeforces.com/problemset/submission/1687/159699643"
        json_data = get_all_testcase(submission_url)
        with open("test_submit_source_format.json", "w") as f:
            json.dump(json_data, f)
        print(json_data)

    run()
