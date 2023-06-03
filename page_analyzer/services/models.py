import psycopg2
from datetime import datetime


class DBUrlsModel():

    def __init__(self, connection):
        self.conn = connection

    def get_url(self, id):
        SQL = f"SELECT * FROM urls WHERE id={id}"

        with self.conn:
            with self.conn.cursor() as curs:
                curs.execute(SQL)
                row = curs.fetchone()
                if row:
                    return {'id': row[0], 'name': row[1],
                            'created_at': datetime.date(row[2])
                            }
                return

    def find_url(self, url):
        SQL = 'SELECT id FROM urls WHERE name LIKE %s'
        with self.conn:
            with self.conn.cursor() as curs:
                curs.execute(SQL, (url,))
                id = curs.fetchone()
                if id:
                    return id[0]
                return

    def get_urls_list(self):
        SQL = "SELECT * FROM urls ORDER BY created_at DESC"

        with self.conn:
            with self.conn.cursor() as curs:
                curs.execute(SQL)
                rows = curs.fetchall()
                return rows

    def save_and_get_id(self, url):
        SQL = ("INSERT INTO urls (name, created_at) "
               "VALUES (%s, %s) RETURNING id")

        data = (url, datetime.now())

        with self.conn:
            with self.conn.cursor() as curs:
                try:
                    curs.execute(SQL, data)
                    return curs.fetchone()[0]
                except psycopg2.IntegrityError:
                    return


def db_connect(db_url):
    try:
        connection = psycopg2.connect(db_url)
        return connection
    except psycopg2.Error as err:
        print("Error: ", err.pgerror)
