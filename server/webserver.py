from server.config import *
from server.excel_handler import get_users_from_excel
from fastapi import FastAPI, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Optional
import uvicorn

app = FastAPI()

app.mount("/static", StaticFiles(directory="client/static"), name="static")
templates = Jinja2Templates(directory="client")

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

users = get_users_from_excel(OUTPUT_FILE_PATH)
users_entrance = {}


def has_permission(password: str):
    if password is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password required")
    if password != ADMIN_PASSWORD:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
    else:
        return True


@app.get("/", response_class=HTMLResponse)
async def root(request: Request, ticket_id: int):
    return templates.TemplateResponse("index.html", {"request": request,
                                                     "ticket_id": ticket_id,
                                                     "base_url": DOMAIN_NAME,
                                                     "page_title": PAGE_TITLE,
                                                     "event_name": EVENT_NAME})


@app.get("/ticket/all")
async def read_all_items(password: Optional[str] = None):
    if has_permission(password):
        return users


@app.get("/ticket/{ticket_id}")
async def read_items(ticket_id: int):
    for user in users:
        if user['ticket_id'] == ticket_id:
            return user
    raise HTTPException(status_code=404, detail="User Not Found")


@app.get("/reception", response_class=HTMLResponse)
async def reception_page(request: Request):
    return templates.TemplateResponse("reception.html", {"request": request,
                                                         "page_title": PAGE_TITLE})


@app.get("/reception/{ticket_id}")
async def verify_ticket(ticket_id: int, password: Optional[str] = None):
    if has_permission(password):
        for user in users:
            if user['ticket_id'] == ticket_id:
                if ticket_id in users_entrance:
                    users_entrance[ticket_id] += 1
                else:
                    users_entrance[ticket_id] = 1

                return {
                    'first_name': user['first_name'],
                    'last_name': user['last_name'],
                    'entrance_count': users_entrance[ticket_id]
                }


@app.get("/camera")
async def has_camera_permission(password: Optional[str] = None):
    if has_permission(password):
        return {'has_camera_perm': True}


def run_server():
    uvicorn.run(app, host="0.0.0.0", port=8000)
