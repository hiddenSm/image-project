# wait_for_db.py
import time
import psycopg2
from psycopg2 import OperationalError

def wait_for_db():
    while True:
        try:
            conn = psycopg2.connect(
                dbname="testdb",
                user="root",
                password="1234",
                host="mypostgres",
                port="5432" # env.port
            )
            conn.close()
            break
        except OperationalError:
            print("Database is unavailable, waiting 5 seconds...")
            time.sleep(5)

if __name__ == "__main__":
    wait_for_db()
