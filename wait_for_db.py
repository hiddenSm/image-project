import time
from psycopg2 import OperationalError
from decouple import config

def wait_for_db():
    while True:
        try:
            conn = psycopg2.connect(
                dbname=config('DATABASE_NAME'),
                user=config('DATABASE_USER'),
                password=config('DATABASE_PASSWORD'),
                host=config('DATABASE_HOST'),
                port=config('DATABASE_PORT')
            )
            conn.close()
            break
        except OperationalError:
            print("Database is unavailable, waiting 5 seconds...")
            time.sleep(5)

if __name__ == "__main__":
    wait_for_db()