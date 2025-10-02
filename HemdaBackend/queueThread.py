import time
import pandas as pd

import query
import shared_data
import sendEmail

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
                data = item["data"]
                df_emails_to_send = data[data['selectEmailSend']]
                sendEmail.sendEmailPrepareAndSend(df_emails_to_send)
                # for col in table_columns[5:13]:
                #      dataDdataF[col] = pd.to_datetime(data[col])
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

                datatuple = list(data.to_records(index=False))
                for row in datatuple:
                    query.setTestsBoardDB(conn, row)
                pass
            shared_data.my_queue.task_done()

            pass
        time.sleep(0.01)  # Wait for 0.1 seconds before checking again
