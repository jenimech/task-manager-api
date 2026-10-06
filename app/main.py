from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class ProjectCreate(BaseModel):
    name: str
    description: str

class Project(BaseModel):
    id: int
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
def create_project(project: ProjectCreate):
    project_id = len(projects) + 1
    new_project = Project(
        id=project_id,
        name=project.name,
        description=project.description
    )
    projects.append(new_project)
    return new_project

@app.get("/projects/{project_id}")
def get_project(project_id: int):
    for project in projects:
        if project.id == project_id:
            return project
    raise HTTPException(
        status_code=404,
        detail="Project not found"
    )