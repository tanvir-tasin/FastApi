from fastapi import FastAPI,Path,HTTPException
import json


api=FastAPI()

def load_data():
    with open('patients.json','r') as f:
        data=json.load(f)
    return data


@api.get('/patients/{patient_id}')

def view_patients(patient_id: str = Path(..., description='Id of patients', examples=['P001'])):
    data=load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404,detail="Patient not found")