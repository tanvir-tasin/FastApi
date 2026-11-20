from fastapi import FastAPI,HTTPException
import json
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field
from typing import Annotated, Literal,Optional


app=FastAPI()

    
    
    

class patient(BaseModel):
    id: Annotated[str, Field(..., description='id of the patient',example=['P001'])]
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
        if self.bmi<18.5:
            return 'underweight'
        elif self.bmi <25:
            return 'fit'
        else:
            return 'obese'
        
class patientupdateC(BaseModel):
    id: Annotated[Optional[str], Field(default=None)]
    name : Annotated[Optional[str], Field(default=None)]
    city : Annotated[Optional[str], Field(default=None)]
    age : Annotated[Optional[int], Field(default=None,gt=0)]
    gender : Annotated[Optional[Literal['male','female','others']] , Field(default=None)]
    height: Annotated[Optional[float], Field(default=None,gt=0)]
    weight:Annotated[Optional[float], Field(default=None,gt=0)]
    
  
@app.delete('/delete/{patient_id}')
def delete(patient_id:str):
    data=load_data()
    if patient_id not in data:
        raise HTTPException(status_code=400,detail='patient id invalid')
    del data[patient_id]
    save_data(data)
    
    return JSONResponse(content='Patient info deleted successfully',status_code=200)   


@app.put('/edit/{patient_id}')
def update_patient(patient_id:str,patient_update:patientupdateC):
    data=load_data()
    if patient_id not in data:
        raise HTTPException(status_code=400,detail='patient id invalid')
    
    existing_patient=data[patient_id]
    #make the patient data from usr a dictonary
    updated_patient_info= patient_update.model_dump(exclude_unset=True)
    #iterate through the data
    
    for key,value in updated_patient_info.items():
        existing_patient[key]=value
        
    #existing data doesn't have id so in pydantic it will raise an error
    existing_patient['id']=patient_id  
    #makeing pydantic object for whole data and for bmi and verdict
    pydantic_patient_object=patient(**existing_patient)
    existing_patient=pydantic_patient_object.model_dump(exclude={'id'})
    #add this dictionary data to json file
    data[patient_id]=existing_patient
    save_data(data)
    
    return JSONResponse(content='updated successfully',status_code=200)
    
    
        
    
    
    
    
    
    
    
    
    
def load_data():
    with open('patients.json','r') as f:
        data=json.load(f)
    return data
def save_data(data):
    with open('patients.json','w') as f:
        json.dump(data,f)