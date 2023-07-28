from enum import Enum
from typing import List, Optional

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from pydantic_web_editor import WebEditorConfig, copy_static_folder

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
copy_static_folder(copy_path="static")


class Hobby(str, Enum):
    SPORTS = "sports"
    NETFLIX = "netflix"


class Student(BaseModel):
    name: str = Field(description="Name of the student.")
    classes: List[str]
    hobby: Hobby
    homework: Optional[bool] = None


@app.get("/")
def hello():
    web_editor_config = WebEditorConfig(title="Example Pydantic Editor", model=Student, start_val=Student(name="Ruth", classes=["chemistry", "math"], hobby=Hobby("netflix")).dict())
    return HTMLResponse(web_editor_config.html)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
