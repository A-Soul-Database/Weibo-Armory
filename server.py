from typing import final
from fastapi import FastAPI
from threading import Thread
import requests
import json
import time
import uvicorn
app = FastAPI(
    openapi_url="/weibo/openapi",
    docs_url="/weibo/docs",
)

Main_Data = {}
Main_Times = 0
Cure_Times = 0
Cure_Text = ""

def Count(fn):
    global Main_Times
    Main_Times += 1
    return fn

def update():
    url = "https://raw.githubusercontent.com/A-Soul-Database/Weibo-Armory/main/assets/"
    while True:
        global Main_Data , Cure_Text
        Main_Data = requests.get(url+"main_data.json").json()
        r = requests.get(url+"cure.txt")
        r.encoding = "utf-8"
        Cure_Text = r.text
        #Main_Data = json.loads(open("assets/main_data.json","r",encoding="utf-8").read())
        #Cure_Text = open("assets/cure.txt", "r" , encoding="utf-8").read()
        time.sleep(60)

@Count
@app.get("/weibo/")
def root():
    global Main_Times
    Main_Times+=1
    return {"code":"0","data":Main_Data}

@Count
@app.get("/weibo/stastics")
def stastics():
    global Main_Times , Cure_Times
    return {"code":"0","data":{"Main_Times":Main_Times,"Cure_Times":Cure_Times}}

@Count
@app.get("/weibo/cure")
def Cure():
    global Cure_Times
    Cure_Times += 1
    try:
        Target_text = Cure_Text[Cure_Times*15:(Cure_Times+1)*15]
    except IndexError:
        Cure_Times = 0
        Target_text = Cure_Text[Cure_Times*15:(Cure_Times+1)*15]
    finally:
        return {"code":"0","data":Target_text}

if __name__ == "__main__":
    t = Thread(target=update)
    t.start()
    uvicorn.run(app, host="0.0.0.0", port=8000)
