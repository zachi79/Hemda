import time

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

            shared_data.my_queue.task_done()

            pass
        time.sleep(0.01)  # Wait for 0.1 seconds before checking again
