import datetime
from dateutil.relativedelta import relativedelta
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()

security = HTTPBasic()

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


@app.get("/start", response_class=HTMLResponse)
def read_items():
    return """
    <html>
        <h1>The unix epoch started at 1970-01-01</h1>
    </html>
    """


@app.post("/check", response_class=HTMLResponse)
def check(credentials: HTTPBasicCredentials = Depends(security)):
    name = str(credentials.username)
    birth_date = str(credentials.password)
    try:
        birth_date = datetime.datetime.strptime(birth_date, '%Y-%m-%d')
    except ValueError:
        raise HTTPException(status_code=401)
    z = datetime.datetime.utcnow() - relativedelta(years=16)
    if z < birth_date:
        raise HTTPException(status_code=401)
    today = datetime.date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return f"""
    <html>
        <h1>Welcome {name}! You are {age}</h1>
    </html>
    """


@app.get("/info")
def get_info(request: Request, format: str = None):
    if not format:
        raise HTTPException(status_code=400)
    x = request.headers.get('user-agent')
    if format == 'json':
        return  {"user_agent": x}
    elif format == 'html':
        html_content = f'<input type="text" id=user-agent name=agent value="{x}">'
        return HTMLResponse(content=html_content, status_code=200)
    else:
        raise HTTPException(status_code=400)

list_of_routes = set()

@app.put("/save/{string}", status_code=200)
def put_save(string: str):
    list_of_routes.update([string])
    return

@app.get("/save/{string}", status_code=404)
def get_save(request: Request, string: str):
    if string in list_of_routes:
        url = request.url_for("get_info")
        return RedirectResponse(status_code=301, url=url)

@app.delete("/save/{string}")
def delete_save(string: str):
    list_of_routes.remove(string)
    return

@app.post("/save/{string}", status_code=400)
def post_save(string: str):
    return



