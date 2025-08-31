import psycopg2

def sendGetData(conn, query):
    data = None
    cur = conn.cursor()
    try:
        cur.execute(query)
        print("Query executed successfully.")
        data = cur.fetchall()
    except psycopg2.ProgrammingError as e:
        print(f"Error executing query: {e}")
    finally:
        cur.close()
    return data

def sendSetNewTeacherData(conn, query, data):
    cursor = conn.cursor()
    data = (data.name, data.phone, data.profession)
    cursor.execute(query, data)
    conn.commit()
    cursor.close()
    return