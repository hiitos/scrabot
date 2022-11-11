from fastapi.responses import JSONResponse
import json
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel  # リクエストbodyを定義するために必要
from src import app as sa

import os
from dotenv import load_dotenv
load_dotenv()

router = APIRouter()
TOKEN = os.getenv('Bot_User_OAuth_Token')
CHANNEL = os.getenv('CHANNEL')

app = sa.SlackApp(
        TOKEN,  # API Token
        CHANNEL 
    )

# リクエストbodyを定義
class slackvari(BaseModel):
    token: str
    challenge: str
    type: str

@router.post("/")
def events(req:slackvari):
  app.submit_text('mentionされました？')
  return JSONResponse({"challenge": req.challenge}, status_code=200)

@router.post("/submit_text", status_code=200)
def text_to_slack(text: str):
  try:
    app.submit_text(text)
    return JSONResponse({"message": "Message sent to Slack."}, status_code=200)
  except Exception:
    return JSONResponse({"message": "Failed to send message."}, status_code=404)

@router.get("/latest-text")
def text_to_slack():
  try:
    app = sa.SlackApp(
        TOKEN,  # API Token
        CHANNEL 
    )
    latest_text = app.part_get()
    return JSONResponse({"message": latest_text}, status_code=200)
  except Exception:
    return JSONResponse({"message": "Failed to read latest message."}, status_code=404)