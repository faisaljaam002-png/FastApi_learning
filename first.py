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

@app.get("/patient/{patient_id}")
def view_patient(patient_id: str):
	data = get_data()

	if patient_id in data:
		return data[patient_id]
	return {"error":"patient not found"}