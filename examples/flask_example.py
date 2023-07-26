from enum import Enum
from typing import List

from flask import Flask, send_from_directory
from pydantic import BaseModel, Field

from pydantic_web_editor import WebEditorConfig, copy_static_folder

app = Flask(__name__)
copy_static_folder(copy_path="static")


class Hobby(Enum):
    SPORTS = "sports"
    NETFLIX = "netflix"


class Student(BaseModel):
    name: str = Field(description="Name of the student.")
    classes: List[str]
    hobby: Hobby


@app.route("/")
def hello():
    web_editor_config = WebEditorConfig(
        title="Example Pydantic Editor", model=Student, load_static="remote"
    )
    return web_editor_config.html


@app.route("/static/<path:filename>")
def serve_static(filename):
    return send_from_directory("static", filename)


if __name__ == "__main__":
    app.run(port=8000)
