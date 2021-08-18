from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()


class Driver(BaseModel):
    version: str
    download_link: str
    tags: List[str] = []


drivers = {
    1: {"version": "6.2.2", "download_link": "https://some-download.com/6.2.2"},
    2: {"version": "5.0.0", "download_link": "https://some-download.com/5.0.0"},
    3: {"version": "4.0.0", "download_link": "https://some-download.com/4.0.0"},
}


@app.get("/wacom-drivers", status_code=200)
def get_drivers():
    return drivers


@app.get("/wacom-drivers/{driver_id}", status_code=200)
def get_driver(driver_id: int):
    driver = drivers.get(driver_id)
    if driver is None:
        raise HTTPException(status_code=404, detail="Driver not found")
    return driver
