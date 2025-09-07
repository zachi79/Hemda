from dbmain import *


def getTeacherListFromDB(conn):
    query = "SELECT * FROM public.teachers ORDER BY user_id ASC"
    data = sendGetData(conn, query)
    return data

def setNewTeacher(conn, data):
    query = "INSERT INTO public.teachers (teachername, phone, profession) VALUES (%s, %s, %s)"
    data = (data.name, data.phone, data.profession)
    data = sendSetData(conn, query, data)
    return data

def getSchoolsListFromDB(conn):
    query = "SELECT * FROM public.schools ORDER BY schoolname ASC"
    data = sendGetData(conn, query)
    return data

def getRoomsListFromDB(conn):
    query = "SELECT * FROM public.rooms ORDER BY roomnumber ASC "
    data = sendGetData(conn, query)
    return data

def getFixedTimeTableDB(conn):
    query = "SELECT * FROM public.fixed_timetable ORDER BY user_id ASC"
    data = sendGetData(conn, query)
    return data


def setFixedTimeTableDB(conn, data):
    data_to_insert = (
        data.day_of_week,
        data.start_time,
        data.end_time,
        data.yearSelect,
        data.teacher_name,
        data.profession,
        data.schoolName,
        data.schoolClass,
        data.room_number
    )

    query = """
        INSERT INTO public.fixed_timetable (
            day_of_week, start_time, end_time, yearSelect, teacher_name, 
            profession, schoolName, schoolClass, room_number
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    sendSetData(conn, query, data_to_insert)
    return data

def delFixedTimeTableDB(conn, data):
    query = "DELETE FROM fixed_timetable WHERE day_of_week = %s"
    data = sendSetData(conn, query, data)
    return data
