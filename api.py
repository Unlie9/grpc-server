import typing as t
from fastapi import Depends, FastAPI, status, HTTPException
from fastapi.responses import JSONResponse


app = FastAPI()


@app.get("/")
async def ping():
    return {"ping": True}