import os
import json
import shutil
from enum import Enum
from typing import List, Optional, Type, get_type_hints, Any, Union

from jinja2 import Environment, PackageLoader
from pydantic import BaseModel, create_model, TypeAdapter

# from sqlmodel import SQLModel


ENV = Environment(loader=PackageLoader("pydantic_web_editor"))
EDITOR_TEMPLATE = ENV.get_template("pydantic_web_editor.html")


# def sqlmodel_to_pydantic(sql_model: Type[SQLModel]) -> Type[BaseModel]:
#     type_hints = get_type_hints(sql_model)
#     Model = create_model("Model", **type_hints)
#     instance = Model(**sql_model.dict())
#     return instance


def copy_static_folder(copy_path: str, create: bool = False):
    """
    Recursively copy a static folder from a pip package to a static folder on a relative path.

    Parameters:
        copy_path: str (str): The relative path where the static folder will be copied.
        create: bool: If True, the directory structure is created if it does not exist.
                      If False and the directory does not exist, a ValueError is raised.

    Returns:
        None
    """
    # Get the absolute path to the static folder in the pip package
    package_path = os.path.dirname(__import__("pydantic_web_editor").__file__)
    static_path = os.path.join(package_path, "static")

    # Check if the destination directory exists, create if necessary and allowed
    if not os.path.exists(copy_path):
        if create:
            os.makedirs(copy_path, exist_ok=True)
        else:
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
    load_static: Optional[LoadStaticType] = LoadStaticType.REMOTE
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

import json

def parse_json_schema(schema, base_path="#"):
    elements = []

    def parse_object(obj, path):
        if 'properties' in obj:
            for prop, value in obj['properties'].items():
                new_path = f"{path}/properties/{prop}"
                elements.append({
                    "type": "Control",
                    "scope": new_path,
                    "label": prop
                })
                parse_object(value, new_path)
        elif 'items' in obj and isinstance(obj['items'], dict):  # For arrays
            # Handle $ref in items
            if '$ref' in obj['items']:
                ref_path = obj['items']['$ref']
                ref_obj = resolve_ref(schema, ref_path)
                parse_object(ref_obj, path)
            else:
                parse_object(obj['items'], path)

    def resolve_ref(schema, ref_path):
        # Resolve a $ref to the actual object it refers to
        parts = ref_path.split('/')[1:]  # Skip the leading '#'
        ref_obj = schema
        for part in parts:
            ref_obj = ref_obj[part]
        return ref_obj

    # Start parsing from the root
    parse_object(schema, base_path)

    return {
        "type": "VerticalLayout",
        "elements": elements
    }



class WebEditorConfig2(BaseModel):
    title: str
    model: Union[BaseModel, Any]
    static_mount: str = "static"
    ui_schema: Optional[str] = None
    gen_ui_schema: Optional[bool] = None

    @property
    def html(self):
        if issubclass(self.model, BaseModel):
            schema = self.model.model_json_schema()
        elif isinstance(self.model, TypeAdapter):
            schema =  self.model.json_schema()
        else:
            raise ValueError("can only generate schema from BaseModel or TypeAdapter")
        
        if self.gen_ui_schema:
            ui_schema = parse_json_schema(schema=schema)
            
        return EDITOR_TEMPLATE.render(
            title=self.title,
            json_schema=schema,
            static_mount=self.static_mount,
            #ui_schema=self.ui_schema,
        )


