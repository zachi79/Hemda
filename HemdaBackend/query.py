from dbmain import *


def getTeacherListFromDB(conn):
    query = "SELECT * FROM public.teachers ORDER BY user_id ASC"
    data = sendGetData(conn, query)
    return data

def setNewTeacher(conn, data):
    query = "INSERT INTO public.teachers (teachername, phone, profession) VALUES (%s, %s, %s)"
    data = sendSetNewTeacherData(conn, query, data)
    return data

def getSchoolsListFromDB(conn):
    query = "SELECT * FROM public.schools ORDER BY schoolname ASC"
    data = sendGetData(conn, query)
    return data

def getRoomsListFromDB(conn):
    query = "SELECT * FROM public.rooms ORDER BY roomnumber ASC "
    data = sendGetData(conn, query)
    return data
