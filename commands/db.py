from os.path import isfile
from sqlite3 import connect

DB_PATH = "./data/db/roran.db"
BUILD_PATH ="./data/db/build.sql"

conn = connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()

def with_commit(func):
    def inner(*args, **kwargs):
        func(*args,**kwargs)
        commit()
        

@with_commit
def build():
    if isfile(BUILD_PATH):
        scriptexec(BUILD_PATH)

def commit():
    conn.commit()

def close():
    conn.close()

def field(command, *values):
    conn.execute(command, tuple(values))    
