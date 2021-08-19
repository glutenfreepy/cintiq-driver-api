from decouple import config
from deta import Deta
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from wacom import get_latest_driver

DB_NAME = config('DB_NAME')

app = FastAPI()
deta = Deta()
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
    driver = drivers.get(key)
    if driver is None:
        raise HTTPException(status_code=404, detail="Driver not found")
    return driver


@app.lib.cron()
def get_and_load_drivers(event):
    get_latest_driver()
