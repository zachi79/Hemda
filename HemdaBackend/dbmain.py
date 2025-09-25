import psycopg2
from psycopg2 import extras

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

def sendSetData(conn, query, data):
    cursor = conn.cursor()
    cursor.execute(query, data)
    conn.commit()
    cursor.close()
    return

