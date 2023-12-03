from enum import Enum
from typing import List, Optional

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from schorg.AboutPage import AboutPage

from pydantic_web_editor import WebEditorConfig, copy_static_folder

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
copy_static_folder(copy_path="static")


@app.get("/")
def hello():
    web_editor_config = WebEditorConfig(
        title="Example Pydantic Editor demoing Schema Org's About Page",
        model=AboutPage,
        start_val={},
    )
    return HTMLResponse(web_editor_config.html)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
