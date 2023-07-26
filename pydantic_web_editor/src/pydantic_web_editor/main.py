import os
import shutil
from enum import Enum
from typing import List, Optional, Type

from jinja2 import Environment, PackageLoader
from pydantic import BaseModel

ENV = Environment(loader=PackageLoader("pydantic_web_editor"))
EDITOR_TEMPLATE = ENV.get_template("pydantic_web_editor.html")


def copy_static_folder(copy_path: str):
    """
    Recursively copy a static folder from a pip package to a static folder on a relative path.

    Parameters:
        package_name (str): The name of the pip package containing the static folder.
        source_folder (str): The relative path of the static folder inside the pip package.
        copy_path: str (str): The relative path where the static folder will be copied.

    Returns:
        None
    """
    # Get the absolute path to the static folder in the pip package
    package_path = os.path.dirname(__import__("pydantic_web_editor").__file__)
    static_path = os.path.join(package_path, "static")

    if not os.path.exists(copy_path):
        raise ValueError(f"Copy destination: {copy_path} does not exist!")

    shutil.copytree(static_path, copy_path, dirs_exist_ok=True)


class Button(BaseModel):
    id: str
    path: str
    text: Optional[str] = "Submit"
    div_classes: Optional[str] = "row mt-2 p-3"
    classes: Optional[str] = "btn"
    verb: Optional[str] = "POST"
    request_kwargs: Optional[str] = "'values': {'payload': payload}"


class LoadStaticType(Enum):
    REMOTE = "remote"
    SKIP = "skip"
    BUNDLED = "bundled"


JSON_EDITOR_CONFIG_DEFAULT = {
    "object_layout": "normal",
    "template": "default",
    "show_errors": "interaction",
    "required_by_default": 1,
    "keep_oneof_values": 1,
    "prompt_before_delete": 1,
    "lib_simplemde": 1,
    "lib_dompurify": 1,
}


class WebEditorConfig(BaseModel):
    title: str
    model: Type[BaseModel]
    start_val: Optional[dict] = {}
    buttons: Optional[List[Button]] = []
    theme: Optional[str] = "bootstrap5"
    iconlib: Optional[str] = "jqueryui"
    load_static: Optional[LoadStaticType] = LoadStaticType.BUNDLED
    static_mount: Optional[str] = "static"
    json_editor_config: Optional[dict] = JSON_EDITOR_CONFIG_DEFAULT

    @property
    def html(self):
        return EDITOR_TEMPLATE.render(
            load_static=self.load_static.value,
            static_mount=self.static_mount,
            theme=self.theme,
            iconlib=self.iconlib,
            buttons=self.buttons,
            json_editor_config={
                "title": self.title,
                "schema": self.model.model_json_schema(),
                "startval": self.start_val,
                "config": self.json_editor_config,
            },
        )
