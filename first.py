from fastapi import FastAPI , Path , HTTPException , Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel , Field , computed_field
from typing import Annotated , Literal
import json

app = FastAPI()

class Patient(BaseModel):
	id : Annotated[str,Field(...,description="Id of the Patient.",examples=["p001"])]
	name : Annotated[str,Field(...,description="Name of the patient.")]
	city : Annotated[str,Field(...,description="Name of the city.")]
	age : Annotated[int,Field(...,lt=100,gt=0,description="Age of Patient.")]
	gender : Annotated[Literal["Male","Female","Others"],Field(...,description="Gender Of The Patient.")]
	height : Annotated[float,Field(...,description="Height of Patient In Meters.")]
	weight : Annotated[float,Field(...,description="weigth of Patient in Kgs.")]

	@computed_field
	@property
	def bmi(self) -> float:
		bmi=round(self.weight/self.height**2,2)
		return bmi

	@computed_field
	@property
	def verdict(self) -> str:

		if self.bmi < 18.9:
			return "Underweight"
		elif self.bmi < 25:
			return "Normal"
		elif self.bmi < 30:
			return "Normal"
		else:
			return "Obese"
		
def get_data():
	with open("patients.json","r") as p:
		data=json.load(p)
		return data

def save_data(data):
	with open("patients.json","w") as p:
		json.dump(data,p)


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
def view_patient(patient_id: str =Path(..., description=("Patient id from database"),example=("p001"))):
	data = get_data()

	if patient_id in data:
		return data[patient_id]
	raise HTTPException(status_code=404,detail="Patient Not Found!")

@app.get('/sort')
def sort_patients(sort_by: str = Query(..., description='Sort on the basis of height, weight or bmi'), order: str = Query('asc', description='sort in asc or desc order')):

    valid_fields = ['height', 'weight', 'bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f'Invalid field select from {valid_fields}')
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='Invalid order select between asc and desc')
    
    data = get_data()

    sort_order = True if order=='desc' else False

    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)

    return sorted_data

@app.post("/create")
def create_patient(patient : Patient):
	data=get_data()
#checking if patient already exists
	if patient.id in data:
		raise HTTPException(status_code=400,detail="Patient Already Exists.")
#saving new data
	data[patient.id]=patient.model_dump(exclude="id")
#creating json
	save_data(data)

	return JSONResponse(status_code=201,content={"Message": "Patient Created successfully."})
