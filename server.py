from fastapi import FastAPI
from threading import Thread
import requests
import time
import uvicorn
app = FastAPI(
    openapi_url="/weibo/openapi",
    docs_url="/weibo/docs",
)

Data = {}
Times = 0

def Count(fn):
    global Times
    Times += 1
    return fn

def update():
    url = "https://raw.githubusercontent.com/A-Soul-Database/Weibo-Armory/main/words.json"
    while True:
        global Data
        Data = requests.get(url).json()
        time.sleep(60)

@Count
@app.get("/weibo/")
def root():
    global Times
    Times+=1
    return {"code":"0","data":Data}

@Count
@app.get("/weibo/stastics")
def stastics():
    global Times
    return {"code":"0","data":Times}

if __name__ == "__main__":
    t = Thread(target=update)
    t.start()
    uvicorn.run(app, host="0.0.0.0", port=8000)
