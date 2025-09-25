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
    query = "SELECT * FROM public.fixed_timetable ORDER BY day_of_week ASC "
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
    data_to_del = (
        data.room_number,
        data.start_time,
        data.end_time
    )

    query = """
        DELETE FROM public.fixed_timetable
        WHERE
            room_number = %s AND
            start_time = %s AND
            end_time = %s;
    """
    data = sendSetData(conn, query, data_to_del)
    return data


def getTestsBoardDB(conn):
    SCHEMA_NAME = 'public'
    TABLE_NAME = 'testsboard'
    query = f"SELECT * FROM {SCHEMA_NAME}.{TABLE_NAME}"
    data = sendGetData(conn, query)
    return data

def delTestsBoardDB(conn):
    SCHEMA_NAME = 'public'
    TABLE_NAME = 'testsboard'
    query = f"TRUNCATE TABLE {SCHEMA_NAME}.{TABLE_NAME}"
    data = sendGetData(conn, query)
    return data

def setTestsBoardDB(conn, dfData):
    SCHEMA_NAME = 'public'
    TABLE_NAME = 'testsboard'
    # --- 4. Prepare Data and Insert using execute_values (Efficient Batch Insert) ---

    # Get column names for the INSERT statement
    columns = dfData.columns.tolist()

    # Convert DataFrame to a list of tuples, matching the column order
    # Note: pandas NaT (Not a Time) or None for date columns will be handled as NULL in SQL
    data_to_insert = [tuple(row) for row in dfData.values]

    # Construct the INSERT statement with dynamic column names
    # %s is a placeholder for `psycopg2` values. (VALUES %s) is for execute_values
    query = f"""
    INSERT INTO {SCHEMA_NAME}.{TABLE_NAME} ({', '.join(columns)})
    VALUES %s
    """

    # Use execute_values for efficient batch insertion
    # The 'data_to_insert' list of tuples will replace %s

    #sendSetDFData(conn, query, data_to_insert)
    print(f"\n{len(dfData)} rows inserted successfully using execute_values into {SCHEMA_NAME}.{TABLE_NAME}.")

    return None