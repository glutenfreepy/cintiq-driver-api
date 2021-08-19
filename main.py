from decouple import config
from deta import Deta
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


DETA_PROJECT_KEY = config('DETA_PROJECT_KEY')
DB_NAME = config('DB_NAME')

app = FastAPI()
deta = Deta(DETA_PROJECT_KEY)
db = deta.Base(DB_NAME)


class Driver(BaseModel):
    key: str
    link: str


@app.get("/wacom-drivers", status_code=200)
def get_drivers():
    response = db.fetch()
    drivers = response.items
    return drivers


@app.get("/wacom-drivers/{key}", status_code=200)
def get_driver(key: str):
    driver = db.get(key)
    if driver is None:
        raise HTTPException(status_code=404, detail="Driver not found")
    return driver
