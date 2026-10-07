from fastapi import FastAPI

# database imports set up
from .database import Base, engine

# import routers
from .routers import projects


Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(projects.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
