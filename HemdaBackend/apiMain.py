import json
import datetime

from fastapi import FastAPI, Request
from pydantic import BaseModel

from main import mainServer
from shared_data import my_queue, results_queue

from typing import List, Optional


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

    converted_list = [
        tuple(item.strftime('%H:%M:%S') if isinstance(item, datetime.time) else item for item in sublist)
        for sublist in fixedTimeTable
    ]

    payload = {
        "fixedTimeTable": converted_list
    }
    payload = json.dumps(payload)
    return payload

class TimeTableData(BaseModel):
    day_of_week: str
    start_time: str
    end_time: str
    yearSelect: str
    teacher_name: str
    profession: str
    schoolName: str
    schoolClass: str
    room_number: str


@app.post("/setFixedTimeTable")
def setFixedTimeTable(data: TimeTableData):
    print("setFixedTimeTable")
    payloadToQ = {
        "cmd": "setFixedTimeTable",
        "data": data
    }
    my_queue.put(payloadToQ)
    fixedTimeTable = mainServer.setFixedTimeTable(data)
    payload = {
        "fixedTimeTable": fixedTimeTable
    }
    payload = json.dumps(payload)
    return payload

@app.post("/delFixedTimeTable")
def delFixedTimeTable(data: TimeTableData):
    payloadToQ = {
        "cmd": "delFixedTimeTable",
        "data": data
    }
    my_queue.put(payloadToQ)
    fixedTimeTable = mainServer.delFixedTimeTable(data)
    payload = {
        "fixedTimeTable": fixedTimeTable
    }
    payload = json.dumps(payload)
    return payload



@app.get("/getTestsBoard")
def getTestsBoard():
    testsBoard = mainServer.getTestsBoard()
    payload = {
        "testsBoard": testsBoard
    }
    payload = json.dumps(payload)
    return payload


class TestsBoardRow(BaseModel):
    schoolSelect: str
    classSelect: str
    teacherSelect: str
    profSelect: Optional[str] = None
    roomSelect: str
    test1: Optional[str] = None
    test2: Optional[str] = None
    test3: Optional[str] = None
    test4: Optional[str] = None
    test5: Optional[str] = None
    test6: Optional[str] = None
    matkonetTest: Optional[str] = None
    labTest: Optional[str] = None
    selectEmailSend: bool

@app.post("/setTestsBoard")
async def setTestsBoard(request: Request ):
    try:
        data = await request.json()
        data = json.loads(data)
    except:
        return 400
    testsBoard = mainServer.setTestsBoard(data)

    payloadToQ = {
        "cmd": "setTestsBoard",
        "data": testsBoard
    }
    my_queue.put(payloadToQ)
    return {"message": "Tests board updated successfully."}