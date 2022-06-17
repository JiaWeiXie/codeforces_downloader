import os
import pathlib
import shutil
from tempfile import TemporaryDirectory
from typing import Any, Dict, List, Tuple, Union, Optional

import gradio

from gradio.components import Component

from codeforces_downloader.downloader import get_submit_source_data
from codeforces_downloader.utils import normalization_text

__all__ = [
    "DownloaderInterface",
]


class DownloaderInterface:
    submission_url = "https://codeforces.com/problemset/submission/%s/%s"
    submit_source_url = "https://codeforces.com/data/submitSource"

    def __init__(self):
        self.block = gradio.Blocks()
        self.zip_dir = TemporaryDirectory(prefix="test_zips")

    def zip_test_data(self, data: List[Dict[str, Union[str, Any]]]):
        zip_dir = pathlib.Path(self.zip_dir.name)

        with TemporaryDirectory(prefix="test_data") as dir_name:
            test_dir = pathlib.Path(dir_name)
            for idx, itme in enumerate(data):
                file_index = idx + 1
                index_dir = test_dir / f"{file_index}"
                os.makedirs(index_dir, exist_ok=True)
                inputs = normalization_text(itme["inputs"])
                answer = normalization_text(itme["answer"])

                with open(index_dir / f"{file_index}.in", "w") as in_file:
                    in_file.write(inputs)

                with open(index_dir / f"{file_index}.ans", "w") as ans_file:
                    ans_file.write(answer)

            out_zip = shutil.make_archive(
                os.path.join(zip_dir, "test"),
                'zip',
                root_dir=os.path.join(test_dir),
            )
            return os.path.join(zip_dir, out_zip)

    def form_click(self, problem_id: str, submission_id: str):
        submission_url = self.submission_url % (problem_id, submission_id)
        json_data = get_submit_source_data(submission_url, self.submit_source_url)
        zip_path = self.zip_test_data(json_data)
        return zip_path

    def url_source_click(self, url):
        json_data = get_submit_source_data(url, self.submit_source_url)
        zip_path = self.zip_test_data(json_data)
        return zip_path

    def url_source_tab(self) -> Tuple[List[Component], gradio.Button]:
        with gradio.TabItem("URL Source"):
            url_input = gradio.Textbox(lines=1, label="problem URL")

            button = gradio.Button()

        return [url_input], button

    def form_tab(self) -> Tuple[List[Component], gradio.Button]:
        with gradio.TabItem("Input Form"):
            problem_id_input = gradio.Textbox(lines=1, label="problem_id")
            submission_id_input = gradio.Textbox(lines=1, label="submission_id")
            button = gradio.Button()

        return [problem_id_input, submission_id_input], button

    def build(self):

        with self.block:
            gradio.Markdown("# Try to download CODEFORCES test data.")
            with gradio.Tabs():
                url_tab_inputs, url_tab_bt = self.url_source_tab()
                form_tab_inputs, form_tab_bt = self.form_tab()

            zip_download = gradio.File(
                file_count="single",
                label="Download test data zip",
            )
            url_tab_bt.click(
                fn=self.url_source_click,
                inputs=url_tab_inputs,
                outputs=[zip_download],
            )
            form_tab_bt.click(
                fn=self.form_click,
                inputs=form_tab_inputs,
                outputs=[zip_download],
            )

    def start(self, debug: bool = False, server_port: Optional[int] = None):
        self.build()
        self.block.launch(debug=debug, server_port=server_port)

    def stop(self):
        self.zip_dir.cleanup()
        self.block.close()
