from src.common.sendRequest import sendRequest
import pandas as pd

table_columns = ['schoolSelect',
                     'classSelect',
                     'teacherSelect',
                     'profSelect',
                     'roomSelect',
                     'test1',
                     'test2',
                     'test3',
                     'test4',
                     'test5',
                     'test6',
                     'matkonetTest',
                     'labTest',
                     'selectEmailSend'
                     ]

def prepareTestsBoard():

    schools_data = sendRequest("getSchoolsList", None, "get")
    schoolsList = [school[0] for school in schools_data['schoolsList']]

    rooms_data = sendRequest("getRoomsList", None, "get")
    roomsList = [room[0] for room in rooms_data['roomsList']]

    grades = ['י1', 'י2', 'י3', 'יא1', 'יא2', 'יא3', 'יב1', 'יב2', 'יב3']
    subject = ['כימיה', 'פיסיקה', '']

    teachers_data = sendRequest("getTeacherList", None, "get")
    columns = ['id', 'teachername', 'phone', 'prof', 'email', 'color']
    teachersDataDF = pd.DataFrame(teachers_data['teachers_list'], columns=columns)
    teachersList = teachersDataDF['teachername'].tolist()

    data = sendRequest("getTestsBoard", None, "get")
    if data == None:
        dataDF = pd.DataFrame(columns=table_columns)
    else:
        dataDF = pd.DataFrame(data['testsBoard'], columns=table_columns[:13])
        dataDF['selectEmailSend'] = False
        for col in table_columns[5:13]:
            dataDF[col] = pd.to_datetime(dataDF[col])

    return dataDF, teachersList, schoolsList, roomsList, grades, subject
