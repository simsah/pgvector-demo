import psycopg2

from app.db.config import db_config

def db_config():
    return {
        'dbname': 'vectordb',
        'user': 'testuser',
        'password': 'testpwd',
        'host': '172.20.0.2',  # Specify the Docker container's IP here
        'port': '5432',  # Default PostgreSQL port
    }



def create_db_connection():
    params = db_config()
    try:
        conn = psycopg2.connect(**params)
        print("hello I'm connected")
        return conn
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting", error)
    return None
