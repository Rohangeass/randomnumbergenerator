from fastapi import FastAPI
import random
app=FastAPI()
@app.get("/home")
def read_root():
    return random.random()