from fastapi import FastAPI
from routers import UserRouter,ProjectRouter
from Database.DB_connection import Base, engine

Base.metadata.create_all(bind=engine)


app = FastAPI()
app.include_router(UserRouter.userRouter)
app.include_router(ProjectRouter.projectRouter)
