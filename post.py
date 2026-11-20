from fastapi import FastAPI,Path,HTTPException, Query
import json
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field,model_validator
from typing import Annotated,Literal
app=FastAPI()

class patient(BaseModel):

    id : Annotated[str, Field(..., description='Put your patient Id',examples=['POO1'])]
    name : Annotated[str, Field(..., description='Name of the patient')]
    city : Annotated[str, Field(..., description='City of the patient')]
    age : Annotated[int, Field(..., gt=0,lt=100, description='Age of the patient')]
    gender : Annotated[Literal['male','female','others'] , Field(..., description='Gender of the patient')]
    height: Annotated[float, Field(..., gt=0,description='Height of the patient')]
    weight:Annotated[float, Field(..., gt=0,description='Weight of the patient')]    

    @computed_field
    @property
    def bmi(self)-> float:
        bmi= round(self.weight/(self.height**2),2)
        return bmi

    @computed_field

    @property
    def verdict(self)-> str:
        if self.bmi< 18.5:
            return 'underweight'
        elif self.bmi<25:
            return 'Normal'
        else:
            return 'Obese'

def load_data():
    with open('patients.json','r') as f:
        data=json.load(f)
    return data
def save_data(data):
    with open('patients.json','w') as f:
        json.dump(data,f)

@app.post('/create')
def create_patient(patient1:patient):
    #load existing data
    data=load_data()


    #check if the patient already exists
    if patient1.id in data:
        raise HTTPException(status_code=400,detail='invalid id')
    data[patient1.id]=patient1.model_dump(exclude=['id'])

    #new patient add to the database
    save_data(data)
    return JSONResponse(status_code=201,content={'message': 'Patient created Successfully'})


