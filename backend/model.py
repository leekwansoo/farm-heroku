from pydantic import BaseModel

class Task(BaseModel):
    id: str
    title: str
    desc: str
    checked: bool