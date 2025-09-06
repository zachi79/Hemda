import json

from fastapi import FastAPI
from pydantic import BaseModel

from main import mainServer
from shared_data import my_queue, results_queue

app = FastAPI()

class Teacher(BaseModel):
    phone: str
    profession: str
    name: str


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/getTeacherList")
def get_teachers():
    teachers_list = mainServer.getTeacherList()
    payload = {
        "teachers_list": teachers_list
    }
    payload = json.dumps(payload)
    return payload

@app.post("/setNewTeacher", response_model=Teacher)
def add_new_teacher(teacher: Teacher):
    payloadToQ = {
        "cmd": "setNewTeacher",
        "data": teacher
    }
    my_queue.put(payloadToQ)
    teachersList = mainServer.setTeacherList(teacher)
    """Retrieve the list of all teachers."""
    payload = {
        "teachers_list": teachersList
    }
    payload = json.dumps(payload)
    return payload

@app.delete("/delTeacherFromList/{teacher_id}")
def delete_teacher(teacher_id: int):

    return {"message": "Teacher deleted successfully."}

@app.get("/getSchoolsList")
def getSchoolsList():
    schoolsList = mainServer.getSchoolsList()
    """Retrieve the list of all teachers."""
    payload = {
        "schoolsList": schoolsList
    }
    payload = json.dumps(payload)
    return payload

@app.get("/getRoomsList")
def getRoomsList():
    roomsList = mainServer.getRoomsList()
    """Retrieve the list of all teachers."""
    payload = {
        "roomsList": roomsList
    }
    payload = json.dumps(payload)
    return payload

@app.post("/getFixedTimeTable")
def getFixedTimeTable():
    fixedTimeTable = mainServer.getFixedTimeTable()
    if fixedTimeTable == None:
        fixedTimeTable = []
    payload = {
        "fixedTimeTable": fixedTimeTable
    }
    payload = json.dumps(payload)
    return payload

@app.post("/setFixedTimeTable")
def setFixedTimeTable(data):
    payloadToQ = {
        "cmd": "setNewTimeTable",
        "data": data
    }
    my_queue.put(payloadToQ)
    fixedTimeTable = mainServer.setFixedTimeTable()
    payload = {
        "fixedTimeTable": fixedTimeTable
    }
    payload = json.dumps(payload)
    return payload
