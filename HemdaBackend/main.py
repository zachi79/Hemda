
import threading
import apiMain
import uvicorn
from queueThread import queueThread
from init import MainInit
from query import *


class MainServerClass(MainInit):
    def __init__(self):
        super().__init__()
        self.teacherListDB = None
        self.schoolsListDB = None
        self.roomsListDB = None
        self.fixedTimeTableDB = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()

    def runThread(self) -> None:
        thread = threading.Thread(target=queueThread, args=(self.conn, self.params,))
        thread.daemon = True
        thread.start()

    def runApi(self) -> None:
        uvicorn.run(apiMain.app, host="127.0.0.1", port=self.params.general.port)

    def runAll(self) -> None:
        self.runThread()
        self.runApi()

    def getTeacherList(self):
        if self.teacherListDB == None:
            self.teacherListDB = getTeacherListFromDB(self.conn)
        return self.teacherListDB

    def setTeacherList(self, data):
        print("setTeacherList")
        self.teacherListDB.append((data.profession,data.phone,data.name,len(self.teacherListDB)+1))
        return self.teacherListDB

    def delTeacherFromList(self):
        if self.teacherListDB == None:
            self.teacherListDB = getTeacherListFromDB(self.conn)
        return self.teacherListDB

    def getSchoolsList(self):
        if self.schoolsListDB == None:
            self.schoolsListDB = getSchoolsListFromDB(self.conn)
        return self.schoolsListDB

    def getRoomsList(self):
        if self.roomsListDB == None:
            self.roomsListDB = getRoomsListFromDB(self.conn)
        return self.roomsListDB


    def getFixedTimeTable(self):
        if self.fixedTimeTableDB == None:
            self.fixedTimeTableDB = getFixedTimeTableDB(self.conn)
        return self.fixedTimeTableDB

    def setFixedTimeTable(self, data):

        self.fixedTimeTableDB = setFixedTimeTableDB(self.conn, data)
        return self.fixedTimeTableDB

    def delFixedTimeTable(self, data):

        self.fixedTimeTableDB = delFixedTimeTableDB(self.conn, data)
        return self.fixedTimeTableDB

# Create a global instance of the server.
global mainServer
mainServer = MainServerClass()

if __name__ == '__main__':
    print("Start Hemda Server")
    with mainServer:
        mainServer.runAll()