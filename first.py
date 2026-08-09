from fastapi import FastAPI
import json

app = FastAPI()

def get_data():
	with open("patients.json","r") as p:
		data=json.load(p)
		return data

@app.get("/")
def hello():
	return ("Hello first api.")

@app.get("/about")
def about():
	return ("my name is faisal i am a ml engineer.")