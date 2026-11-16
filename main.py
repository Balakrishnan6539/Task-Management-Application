from fastapi import FastAPI
from routers import UserRouter,ProjectRouter,TaskRouter
from Database.DB_connection import Base, engine
from Database import EventListener

Base.metadata.create_all(bind=engine)


app = FastAPI(title="Team Management Application",)
app.include_router(UserRouter.userRouter)
app.include_router(ProjectRouter.projectRouter)
app.include_router(TaskRouter.taskRouter)
