from config import *
from excel_handler import get_users_from_excel
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
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

users = get_users_from_excel(INPUT_FILE_PATH)


def authenticate(args):
    if args['password'] != ADMIN_PASSWORD:
        raise HTTPException(status_code=400, detail='Incorrect password')


@app.get("/ticket/all")
async def read_all_items(args: Request):
    try:
        args = await args.json()
    except:
        return {"message": "Please provide a password"}

    authenticate(args)
    return users


@app.get("/ticket/{ticket_id}")
async def read_items(ticket_id: int):
    for user in users:
        if user['ticket_id'] == ticket_id:
            return user
    raise HTTPException(status_code=404, detail="User Not Found")


def run_server():
    uvicorn.run(app, host="127.0.0.1", port=8000)
