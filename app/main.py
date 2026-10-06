from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Project(BaseModel):
    name: str
    description: str

projects = []

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/projects")
def get_projects():
    return projects

@app.post("/projects")
def create_project(project: Project):
    projects.append(project)
    return project