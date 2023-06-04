import psycopg2
from data_login import database, user, password

def create_db(cur):
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

        print('[INFO] Таблицы успешно созданы!')

def add_client(cur, name, surname, email):
        cur.execute("INSERT INTO client(name, surname, email) VALUES(%s, %s, %s);",(name, surname, email))

        print('[INFO] Данные успешно добавлены!')

def add_phone(cur, client_id, phone):
        cur.execute("INSERT INTO phones(client_id, phone) VALUES(%s, %s);", (client_id, phone))

        print('[INFO] Номер телефона успешно добавлен!')

def change_client(cur, client_id, name, surname, email, phone):
        cur.execute("UPDATE client SET name = %s, surname = %s, email = %s WHERE id = %s", (name, surname, email, client_id))

        cur.execute("UPDATE phones SET phone = %s WHERE id = %s", (phone,  client_id))

        print('[INFO] Данные успешно изменены!')

def delete_phone(cur, client_id, phone):
        cur.execute("DELETE FROM phones WHERE client_id = %s AND phone = %s", (client_id, phone))

        print('[INFO] Данные успешно удалены!')

def delete_client(cur, client_id):
        cur.execute("DELETE FROM phones WHERE client_id = %s", (client_id,))

        cur.execute("DELETE FROM client WHERE id = %s", (client_id,))

        print('[INFO] Данные успешно удалены!')

def find_client(cur, name, surname, email, phone):
            cur.execute("""SELECT c.name, c.surname, c.email, p.phone FROM client c
                            JOIN phones p ON c.id = p.client_id
                            WHERE name = %s and surname =  %s and email = %s and phone = %s
                            """, (name, surname, email, phone))
            res1 = cur.fetchall()[0]

            print(res1)

if __name__ == '__main__':
    with psycopg2.connect(database=database, user=user, password=password) as conn:
        with conn.cursor() as cur:
            cur.execute("DROP TABLE phones")
            cur.execute("DROP TABLE client")
            create_db(cur)
            add_client(cur,'Алексей','Кравченко','krava@mail.ru')
            add_phone(cur, '1', '89001234567')
            add_phone(cur, '1', '89009999999')
            change_client(cur, "1","Илона","Саркисян","Илоша@майл.ру", '89001234444')
            delete_phone(cur, '1', '89009999999')
            delete_client(cur, '1')
            find_client(cur, 'Илона', 'Саркисян', 'Илоша@майл.ру', '89001234444')