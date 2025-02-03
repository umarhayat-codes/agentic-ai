from fastapi import FastAPI,Body,Path
from pydantic import BaseModel,validator,EmailStr
from re import match

app = FastAPI() 

class Student(BaseModel):
    name:str
    email:EmailStr
    age:int
    courses:list[str]

    @validator('name')
    def len_name(cls,name):
        if not match(r"^[a-zA-Z ]+$",name):
            raise ValueError("name must be character")
        if not (1 <= len(name) <= 50):
            raise ValueError("character must be contain 1-50")
        return name
    
   
    @validator('age')
    def validate_age(cls,age):
        if not (18 < age < 30):
            raise ValueError("age must be 18-30")
        return age
    
    @validator('courses')
    def validate_courses(cls, courses):
        if not (1 <= len(courses) <= 5) :
            raise ValueError("The courses list must have between 1 and 5 courses.")
        if len(set(courses)) != len(courses):
            raise ValueError("Duplicate course names are not allowed.")
        for course in courses:
            if not (5 <= len(course) <= 30):
                raise ValueError("Each course name must be between 5 and 30 characters long.")
        return courses
    
@app.post('/students/register')
async def create(student:Student):
    try:
        return{
            "status":"success",
            "data":student
        }
    except Exception as e:
        return{
            "status":"error",
            "data":None,
            "message":str(e)
        }
    
@app.get('/students/{student_id}')
async def get_student_info(student_id:int, include_grade : bool, semester : str):
    if not (1000 <= student_id <= 9999):
        raise ValueError("Student id must 1000-9999")
    student_data = {"id":1, "name":"umar", "program":"BSCS"}
    if include_grade:
        student_data["grade"] = {
            "Fall2024": {"Math":"B","Physics":"-B"},"Spring2025":{"Computer":"A","Eng":"-B"}
        }
    if not match(r"(Fall|Spring|Summer)\d{4}$",semester):
        raise ValueError("Semester must be in the format Fall2024, Spring2025")
    return student_data

class Email(BaseModel):
    email: EmailStr

@app.put("/students/{student_id}/email")
async def update_student_email(student_id: int, email: Email):
    if 1000 <= student_id <= 9999:
        raise ValueError("student id must be 1000-9999")
    email = email.email
    # updated_email = "abc@gmail.com"
    updated_email = email    
    try: 
        return {
            "message": "Student email updated successfully.",
            "data":{"email":updated_email,"student_id":student_id}
        }
    except Exception as e:
        return {
            "message": str(e),
            "data":None
            
        }