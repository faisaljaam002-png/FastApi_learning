from fastapi import FastAPI
import json

app = FastAPI()

def get_data():
	with open("patients.json","r") as p:
		data=json.load(p)
		return data

@app.get("/")
def hello():
	return ("Patient Mangement System.")

@app.get("/about")
def about():
	return ("A System to add and view patient records.")

@app.get("/view")
def view():
	data = get_data()
	return data