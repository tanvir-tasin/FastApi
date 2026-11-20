
# # pydantic step1
# from pydantic import BaseModel

# class patient(BaseModel):
#     name : str
#     age : int

# def patient_data_info(patient1: patient ):
#     print(patient1.age)
#     print(patient1.name)

# #step 2
# patient_info = {'name':'tas','age':'30'}

# patient2=patient(**patient_info)

# #step 3
# patient_data_info(patient2)

from pydantic import BaseModel , Field , EmailStr , AnyUrl , field_validator,model_validator,computed_field
from typing import Optional, Annotated
class Bird(BaseModel):
    name:Optional[str]= None
    email: EmailStr 
    
    linkedin_url : AnyUrl
    married: Annotated[bool,Field(default=None,title='marriage status',description='Is the bird married or not')]
    colour:list[str] 
    habitat: dict[str,str]
   # age:Annotated[Optional[int],Field(gt=0,lt=30,strict=True)]
    age : int
    @field_validator('email')
    @classmethod
    def email_validator(cls,value):
        valid_domains=['ac.bd','edu.bd']
        domain_name=value.split('@')[-1]
        if domain_name not in valid_domains:
            raise ValueError
        return value
    @field_validator('age',mode='before')
    @classmethod
    def validate_age(cls,value):
        if 0 < value < 100:
            return value
        else:
            raise ValueError('age should be in between 0 and 100')  
    @model_validator(mode='after')
    def emergency_validator(self):
        if self.age > 60 and 'emergency' not in self.habitat:
            raise ValueError('patient older than 60 must have an emergency contact')

    @computed_field
    @property
    def calculate_bmi(self)->float:
        bmi= round(self.age**3.2/(self.age**2),3)
        return bmi



bird1={'colour':'black&white','linkedin_url':'h://googlecom','age':89,'email':'tasin@edu.bd','colour':['Green','Blue'],'habitat':{'1':"Bangladesh",'2':'Canada','emergency':"Dhaka"}}
extract_bird1=Bird(**bird1)


print(extract_bird1.linkedin_url)
print(extract_bird1.married)
print(extract_bird1.age)
print(extract_bird1.calculate_bmi)



