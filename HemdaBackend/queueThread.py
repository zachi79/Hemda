import time
import pandas as pd

import query
import shared_data

def queueThread(conn, params):
    """
    This function continuously checks the queue for new items.

    Args:
        q (queue.Queue): The queue to be checked.
        conn: The connection object to be printed.
    """
    while True:
        if not shared_data.my_queue.empty():
            item = shared_data.my_queue.get()  # Get an item from the queue
            print(f"Queue has an item: {item}")

            if item["cmd"] == "setNewTeacher":
                query.setNewTeacher(conn, item["data"])
                pass
            if item["cmd"] == "setFixedTimeTable":
                query.setFixedTimeTableDB(conn, item["data"])
                pass
            if item["cmd"] == "delFixedTimeTable":
                query.delFixedTimeTableDB(conn, item["data"])
                pass
            if item["cmd"] == "setTestsBoard":
                query.delTestsBoardDB(conn)
                time.sleep(0.2)
                data = pd.DataFrame(item["data"])
                data = data.drop(columns=['selectEmailSend'])
                data = data.rename(columns={
                    'schoolSelect': 'schoolName',
                    'classSelect': 'schoolClass',
                    'teacherSelect': 'teacher_name',
                    'profSelect': 'profession',
                    'roomSelect': 'room_number',
                    'test1': 'test1',
                    'test2': 'test2',
                    'test3': 'test3',
                    'test4': 'test4',
                    'test5': 'test5',
                    'test6': 'test6',
                    'matKonetTest': 'matKonetTest',
                    'labTest': 'labTest'
                })



                query.setTestsBoardDB(conn, data)
                pass
            shared_data.my_queue.task_done()

            pass
        time.sleep(0.01)  # Wait for 0.1 seconds before checking again
