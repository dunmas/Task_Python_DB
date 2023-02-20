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

        conn.commit()


def add_client(conn, first_name, last_name, email, phones=None):
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO client(first_name, last_name, email)
        VALUES(%s, %s, %s)
        RETURNING client_id;
        """, (first_name, last_name, email))
        client_id = cur.fetchone()

        if phones is not None:
            for phone in phones:
                cur.execute("""
                INSERT INTO phone_number(phone, client_id)
                VALUES(%s, %s)
                """, (phone, client_id))

        conn.commit()


def client_id_checker(conn, client_id):
    with conn.cursor() as cur:
        cur.execute("""
        SELECT client_id FROM client
        WHERE client_id = %s
        """, (client_id,))

        return cur.fetchone()


def add_phone(conn, client_id, phone):
    existing_result = client_id_checker(conn, client_id)

    with conn.cursor() as cur:
        if existing_result is not None:
            cur.execute("""
            INSERT INTO phone_number(phone, client_id)
            VALUES(%s, %s);
            """, (phone, client_id))

        conn.commit()


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

    # add_client(conn, 'Post', 'Gre', 'sql@yandex.ru')
    # add_client(conn, 'Saul', 'Goodman', 'sgalb@yahoo.com', ['9876543211', '9871234566'])
    # add_phone(conn, 1, '9876546782')
conn.close()
