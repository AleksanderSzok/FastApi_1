import datetime

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()



@app.get("/")
def read_root():
    return {"start": "1970-01-01"}


@app.get("/method")
def get_item():
    return {"method": "GET"}

@app.put("/method")
def put_item():
    return {"method": "PUT"}

@app.post("/method", status_code=201)
def post_item():
    return {"method": "POST"}

@app.delete("/method")
def delete_item():
    return {"method": "DELETE"}

@app.options("/method")
def options_item():
    return {"method": "OPTIONS"}

@app.get("/day", status_code=200)
def get_day(name: str, number: int):
    days = {1: "monday", 2: "tuesday", 3: "wednesday", 4: "thursday", 5: "friday", 6: "saturday", 7: "sunday"}
    if days.get(number) != name.lower():
        raise HTTPException(status_code=400)

class Item(BaseModel):
    date: str
    event: str

event_list = []

@app.put("/events", status_code=200)
def event(item: Item):
    now = datetime.datetime.now()
    time_added = now.strftime("%Y-%m-%d")
    le = len(event_list)
    new_item = {
        'id': le,
        'name': item.event,
        'date': item.date,
        'date_added': time_added
    }
    event_list.append(new_item)
    return new_item


@app.get("/events/{date}", status_code=200)
def get_event(date: str):
    output_list = []
    try:
        datetime.datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        raise HTTPException(status_code=400)

    for element in event_list:
        if element['date'] == date:
            output_list.append(element)
    if output_list:
        return output_list
    else:
        raise HTTPException(status_code=404)