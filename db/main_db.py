import sqlite3
from db import queries
from config import path_db

def init_db():
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(queries.CREATE_TABLE_TASK)
    print("База данных подключена!")
    conn.commit()
    conn.close()


def add_task(task):
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(queries.INSERT_TASK, (task, ))
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    return task_id


def get_tasks(filter_type=None):
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()

    if filter_type == 'completed': 
        cursor.execute("SELECT id, task, completed FROM tasks WHERE completed = 1")
    elif filter_type == 'uncompleted': 
        cursor.execute("SELECT id, task, completed FROM tasks WHERE completed = 0")
    else:  
        cursor.execute("SELECT id, task, completed FROM tasks")

    tasks = cursor.fetchall()
    conn.close()
    return tasks



def delete_task(task_id):
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(queries.DELETE_TASK, (task_id, ))
    conn.commit()
    conn.close()

def delete_all_tasks():
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks")
    conn.commit()
    conn.close()

def delete_completed_tasks():
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE completed = 1")
    conn.commit()
    conn.close()
    print("Выполненные задачи удалены!")

    
def update_task(task_id, new_task=None, completed=None):
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()

    if new_task is not None:
        cursor.execute(queries.UPDATE_TASK, (new_task, task_id))
    
    if completed is not None:
        cursor.execute("UPDATE tasks SET completed = ? WHERE id = ?", (completed, task_id))

    conn.commit()
    conn.close()
