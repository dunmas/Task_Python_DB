import psycopg2

def create_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS client(
        client_id SERIAL PRIMARY KEY,
        first_name VARCHAR(40) NOT NULL,
        last_name VARCHAR(40) NOT NULL,
        email VARCHAR(40) UNIQUE NOT NULL
        );
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS phone_number(
        phone_id SERIAL PRIMARY KEY,
        phone VARCHAR(10) UNIQUE NOT NULL,
        client_id INTEGER NOT NULL REFERENCES client(client_id)
        );
        """)

def add_client(conn):
    pass

def add_phone(conn):
    pass

def client_edit(conn):
    pass

def delete_phone(conn):
    pass

def delete_client(conn):
    pass

def find_client(conn):
    pass

with psycopg2.connect(database='clients_db', user='postgres', password='zemege50') as conn:
    create_db(conn)

conn.close()
