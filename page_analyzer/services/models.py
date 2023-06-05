import psycopg2
from psycopg2.extras import DictCursor
from datetime import datetime


class DBUrlsModel:

    def __init__(self, db_url):
        self.db_url = db_url
        self.conn = None

    def db_conn(self):
        try:
            self.conn = psycopg2.connect(self.db_url)
        except psycopg2.Error as err:
            print("Error: ", err.pgerror)

    def db_close(self):
        self.conn.close()

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
        SQL = ("SELECT "
               "urls.id, urls.name, MAX(url_checks.created_at) as last_check, "
               "url_checks.status_code "
               "FROM urls LEFT JOIN url_checks ON urls.id = url_checks.url_id "
               "GROUP BY urls.id, url_checks.status_code "
               "ORDER BY urls.created_at DESC")

        with self.conn:
            with self.conn.cursor(cursor_factory=DictCursor) as curs:
                curs.execute(SQL)
                rows = curs.fetchall()
                for row in rows:
                    if row['last_check']:
                        row['last_check'] = datetime.date(row['last_check'])
                return rows

    def add_url(self, url):
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

    def add_check(self, check):
        SQL = ("INSERT INTO url_checks "
               "(url_id, status_code, h1, title, description, created_at) "
               "VALUES "
               "(%(url_id)s, %(status_code)s, %(h1)s, %(title)s, "
               "%(description)s, %(created_at)s) "
               "RETURNING id")
        data = check

        with self.conn:
            with self.conn.cursor() as curs:
                curs.execute(SQL, data)
                return curs.fetchone()

    def get_url_checks(self, id):
        SQL = ("SELECT * FROM url_checks "
               "WHERE url_id=%s ORDER BY created_at DESC")

        with self.conn:
            with self.conn.cursor(cursor_factory=DictCursor) as curs:
                curs.execute(SQL, (id,))
                rows = curs.fetchall()
                for row in rows:
                    row['created_at'] = datetime.date(row['created_at'])
                return rows


def make_urlcheck(url_id, url_name):

    status_code = None
    h1 = None
    title = None
    description = None
    check = {'url_id': url_id, 'status_code': status_code, 'h1': h1,
             'title': title, 'description': description,
             'created_at': datetime.now()
             }
    return check
