from fastapi import FastAPI
import uvicorn
from typing import Union

app = FastAPI()
# uvicorn.run(app, host="0.0.0.0")

@app.get("/")
async def read_root():
    return {"Msg": "World"}
