from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from ..database import SessionLocal
from .. import models
from ..schemas import ProjectCreate, ProjectUpdate


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/projects")
def get_projects(db: Session = Depends(get_db)):
    projects = db.query(models.Project).all()
    return projects


@router.post("/projects")
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    new_project = models.Project(
        name=project.name,
        description=project.description
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return new_project


@router.get("/projects/{project_id}")
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )
    return project


@router.delete("/projects/{project_id}")
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


@router.put("/projects/{project_id}")
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


@router.patch("/projects/{project_id}")
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