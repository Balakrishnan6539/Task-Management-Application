from fastapi import FastAPI
from Database.DB_connection import Base, engine

Base.metadata.create_all(bind=engine)


app = FastAPI()
