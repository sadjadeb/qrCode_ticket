from server.config import *
from server.excel_handler import get_users_from_excel
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import uvicorn

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

users = get_users_from_excel(OUTPUT_FILE_PATH)


def has_permission(password: str):
    if password is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password required")
    if password != ADMIN_PASSWORD:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
    else:
        return True


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


@app.get("/reception/{ticket_id}")
async def verify_ticket(ticket_id: int, password: Optional[str] = None):
    if has_permission(password):
        for user in users:
            if user['ticket_id'] == ticket_id:
                return {'verified': True}


@app.get("/camera")
async def has_camera_permission(password: Optional[str] = None):
    if has_permission(password):
        return {'has_camera_perm': True}


def run_server():
    uvicorn.run(app, host="0.0.0.0", port=8000)
