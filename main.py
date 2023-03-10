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
    if client_id_checker(conn, client_id) is None:
        return

    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO phone_number(phone, client_id)
        VALUES(%s, %s);
        """, (phone, client_id))

        conn.commit()


def client_edit(conn, client_id, first_name=None, last_name=None, email=None, phones=None):
    if client_id_checker(conn, client_id) is None:
        return

    if first_name is not None:
        with conn.cursor() as cur:
            cur.execute("""
            UPDATE client
            SET first_name = %s
            WHERE client_id = %s;
            """, (first_name, client_id))

            conn.commit()

    if last_name is not None:
        with conn.cursor() as cur:
            cur.execute("""
            UPDATE client
            SET last_name = %s
            WHERE client_id = %s;
            """, (last_name, client_id))

            conn.commit()

    if email is not None:
        with conn.cursor() as cur:
            cur.execute("""
            UPDATE client
            SET email = %s
            WHERE client_id = %s;
            """, (email, client_id))

            conn.commit()

    if phones is not None:
        with conn.cursor() as cur:
            cur.execute("""
            DELETE FROM phone_number
            WHERE client_id = %s;
            """, (client_id,))

            for phone in phones:
                cur.execute("""
                INSERT INTO phone_number(phone, client_id)
                VALUES(%s, %s)
                """, (phone, client_id))

            conn.commit()


def delete_phone(conn, client_id, phone):
    if client_id_checker(conn, client_id) is None:
        return

    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM phone_number
        WHERE client_id = %s AND phone = %s;
        """, (client_id, phone))

        conn.commit()


def delete_client(conn, client_id):
    if client_id_checker(conn, client_id) is None:
        return

    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM phone_number
        WHERE client_id = %s;
        """, (client_id,))

        cur.execute("""
        DELETE FROM client
        WHERE client_id = %s;
        """, (client_id,))

        conn.commit()


# ???????????????????? ???????????? ?? ???????????????????? ID ????????????????
def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    result = []

    if first_name is not None:
        with conn.cursor() as cur:
            cur.execute("""
            SELECT client_id FROM client
            WHERE first_name = %s;
            """, (first_name,))

            pairs = cur.fetchall()

            for pair in pairs:
                result.append(pair[0])

            conn.commit()

    if last_name is not None:
        with conn.cursor() as cur:
            cur.execute("""
            SELECT client_id FROM client
            WHERE last_name = %s;
            """, (last_name,))

            pairs = cur.fetchall()

            for pair in pairs:
                result.append(pair[0])

            conn.commit()

    if email is not None:
        with conn.cursor() as cur:
            cur.execute("""
            SELECT client_id FROM client
            WHERE email = %s;
            """, (email,))

            data = cur.fetchall()

            if data:
                result.append(data[0][0])

            conn.commit()

    if phone is not None:
        with conn.cursor() as cur:
            cur.execute("""
            SELECT client_id FROM phone_number
            WHERE phone = %s
            """, (phone,))

            data = cur.fetchall()

            if data:
                result.append(data[0][0])

            conn.commit()

    return result


with psycopg2.connect(database='clients_db', user='postgres', password='zemege50') as conn:
    create_db(conn)

    # add_client(conn, 'Post', 'Gre', 'sql@yandex.ru')
    # add_client(conn, 'Saul', 'Goodman', 'sgalb@yahoo.com', ['9876543211', '9871234566'])
    # add_phone(conn, 1, '9876546782')

    # ???????????????? ?????????????? edit
    # client_edit(conn, 1, 'Anna')
    # client_edit(conn, 1, None, 'Braun')
    # client_edit(conn, 1, None, None, 'braun@yandex.ru')
    # client_edit(conn, 1, None, None, None, ['1111111111', '2222222222'])

    # ???????? ???????????? ID ?????? - ???????????? ???? ????????????????????
    # client_edit(conn, 999, 'Bill')

    # delete_phone(conn, 1, '1111111111')

    # delete_client(conn, 1)

    # add_client(conn, 'Post', 'Gre', 'sql1@yandex.ru')
    # add_client(conn, 'Post', 'Con', 'sql2@yandex.ru')
    # add_client(conn, 'Post', 'Seed', 'sql3@yandex.ru')
    # add_client(conn, 'Gonsales', 'Seed', 'sql4@yandex.ru')

    # print(find_client(conn, 'Post'))
    # print(find_client(conn, None, 'Seed'))
    # print(find_client(conn, None, None, 'sql3@yandex.ru'))
    # print(find_client(conn, None, None, None, '9876543211'))

    # print(find_client(conn, 'None'))

conn.close()
