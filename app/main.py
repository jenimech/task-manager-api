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
next_project_id = 1

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/projects")
def get_projects():
    return projects

@app.post("/projects")
def create_project(project: ProjectCreate):
    global next_project_id
    new_project = Project(
        id=next_project_id,
        name=project.name,
        description=project.description
    )
    projects.append(new_project)
    next_project_id += 1
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

@app.delete("/projects/{project_id}")
def delete_project(project_id: int):
    for project in projects:
        if project.id == project_id:
            projects.remove(project)
            return {"message": "Project deleted successfully"}
    raise HTTPException(
        status_code=404,
        detail="Project not found"
    )


@app.put("/projects/{project_id}")
def update_project(project_id: int, project_data: ProjectCreate):
    for project in projects:
        if project.id == project_id:
            project.name = project_data.name
            project.description = project_data.description
            return project
    raise HTTPException(
        status_code=404,
        detail="Project not found"
    )