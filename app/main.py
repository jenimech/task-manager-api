from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel

# database imports set up
from .database import Base, engine, SessionLocal
from . import models
from sqlalchemy.orm import Session


Base.metadata.create_all(bind=engine)


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class ProjectCreate(BaseModel):
    name: str
    description: str

class ProjectUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/projects")
def get_projects(db: Session = Depends(get_db)):
    projects = db.query(models.Project).all()
    return projects


@app.post("/projects")
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    new_project = models.Project(
        name=project.name,
        description=project.description
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return new_project


@app.get("/projects/{project_id}")
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )
    return project


@app.delete("/projects/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )
    db.delete(project)
    db.commit()
    return {"message": "Project deleted successfully"}


@app.put("/projects/{project_id}")
def update_project(project_id: int, project_data: ProjectCreate, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )
    project.name = project_data.name
    project.description = project_data.description
    db.commit()
    db.refresh(project)

    return project


@app.patch("/projects/{project_id}")
def partial_update_project(project_id: int, project_data: ProjectUpdate, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    if project_data.name is not None:
        project.name = project_data.name
    if project_data.description is not None:
        project.description = project_data.description

    db.commit()
    db.refresh(project)

    return project