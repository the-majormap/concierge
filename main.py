from fastapi import Cookie, FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from app.db.connection import database
from sqlalchemy.orm import Session

from app.apis import subjects, keyword, filters, major as api_major
from app.controllers import major

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request, db: Session = Depends(database)):
    return templates.TemplateResponse("main.html", {"request": request})


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


app.include_router(subjects.router)
app.include_router(keyword.router)
app.include_router(filters.router)
app.include_router(major.router)
app.include_router(api_major.router)
