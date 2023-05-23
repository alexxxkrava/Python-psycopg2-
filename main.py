import psycopg2
from data_login import database, user, password

def create_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS client( 
                id SERIAL PRIMARY KEY,
                name VARCHAR(50),
                surname VARCHAR(50),
                email VARCHAR(80)
                );               
            """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS phones( 
                id SERIAL PRIMARY KEY,
                client_id INT NOT NULL REFERENCES client(id),
                phone VARCHAR(100)
                );               
            """)
        conn.commit()
        print('[INFO] Таблицы успешно созданы!')

def add_client(conn, name, surname, email):
    with conn.cursor() as cur:
        cur.execute("INSERT INTO client(name, surname, email) VALUES(%s, %s, %s);",(name, surname, email))
        conn.commit()
        print('[INFO] Данные успешно добавлены!')

def add_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("INSERT INTO phones(client_id, phone) VALUES(%s, %s);", (client_id, phone))
        conn.commit()
        print('[INFO] Номер телефона успешно добавлен!')

def change_client(conn, client_id, name=None, surname=None, email=None, phone=None):
    with conn.cursor() as cur:
        cur.execute("UPDATE client SET name = %s, surname = %s, email = %s WHERE id = %s", (name, surname, email, client_id))

        cur.execute("UPDATE phones SET phone = %s WHERE id = %s", (phone,  client_id))
        conn.commit()
        print('[INFO] Данные успешно изменены!')

def delete_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM phones WHERE client_id = %s AND phone = %s", (client_id, phone))
        conn.commit()
        print('[INFO] Данные успешно удалены!')

def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM phones WHERE client_id = %s", (client_id,))

        cur.execute("DELETE FROM client WHERE id = %s", (client_id,))

        conn.commit()
        print('[INFO] Данные успешно удалены!')

def find_client(conn, name=None, surname=None, email=None, phone=None):
    with conn.cursor() as cur:
            cur.execute("""SELECT * FROM client c 
                            JOIN phones p ON c.id = p.client_id
                            WHERE name = %s or surname =  %s or email = %s or phone = %s
                            """, (name, surname, email, phone))
            res1 = cur.fetchall()
            print(res1)

if __name__ == '__main__':
    conn = psycopg2.connect(database=database, user=user, password=password)
    with conn.cursor() as cur:
        cur.execute("DROP TABLE phones")
        cur.execute("DROP TABLE client")
        conn.commit()
    create_db(conn)
    add_client(conn,'Алексей','Кравченко','krava@mail.ru')
    add_phone(conn, '1', '89001234567')
    add_phone(conn, '1', '89009999999')
    change_client(conn, "1","Илона","Саркисян","Илоша@майл.ру", '89001234444')
    delete_phone(conn, '1', '89009999999')
    delete_client(conn, '1')
    find_client(conn, "Илона")

    if conn:
        conn.close()
        print('[INFO] Работа закончена!')
