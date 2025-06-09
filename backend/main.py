from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from uuid import uuid4

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class StudentBase(BaseModel):
    name: str
    email: EmailStr
    className: str
    dob: str
    address: str
    parentName: str
    parentPhone: str
    parentEmail: EmailStr

class Student(StudentBase):
    id: str

fake_db = []

@app.post("/students/", response_model=Student)
def create_student(student: StudentBase):
    new_student = Student(id=str(uuid4()), **student.dict())
    fake_db.append(new_student)
    return new_student

@app.get("/students/", response_model=list[Student])
def get_students():
    return fake_db

@app.put("/students/{student_id}/", response_model=Student)
def update_student(student_id: str, student: StudentBase):
    for idx, s in enumerate(fake_db):
        if s.id == student_id:
            updated_student = Student(id=student_id, **student.dict())
            fake_db[idx] = updated_student
            return updated_student
    raise HTTPException(status_code=404, detail="Student not found.")

@app.delete("/students/{student_id}/")
def delete_student(student_id: str):
    for idx, s in enumerate(fake_db):
        if s.id == student_id:
            del fake_db[idx]
            return {"detail": "Student deleted"}
    raise HTTPException(status_code=404, detail="Student not found.")