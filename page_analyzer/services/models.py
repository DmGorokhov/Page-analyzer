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

    def make_sqlquery(self, sql, data=None, fetch=None):
        with self.conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(sql, data)
            match fetch:
                case None:
                    return
                case 'one':
                    return curs.fetchone()
                case 'all':
                    return curs.fetchall()

    def get_url(self, id):
        SQL = f"SELECT * FROM urls WHERE id={id}"
        row = self.make_sqlquery(SQL, fetch='one')
        return row

    def find_url(self, url):
        SQL = 'SELECT id FROM urls WHERE name LIKE %s'
        url_id = self.make_sqlquery(SQL, (url,), fetch='one')
        if url_id:
            return url_id.get('id')
        return

    def get_urls_list(self):
        SQL = ("SELECT "
               "urls.id, urls.name, MAX(url_checks.created_at) as last_check, "
               "url_checks.status_code "
               "FROM urls LEFT JOIN url_checks ON urls.id = url_checks.url_id "
               "GROUP BY urls.id, url_checks.status_code "
               "ORDER BY urls.created_at DESC")

        rows = self.make_sqlquery(SQL, fetch='all')
        return rows

    def add_url(self, url):
        SQL = ("INSERT INTO urls (name, created_at) "
               "VALUES (%s, %s) RETURNING id")

        data = (url, datetime.now())

        with self.conn:
            try:
                added_id = self.make_sqlquery(SQL, data, fetch='one')
                return added_id[0]
            except psycopg2.IntegrityError:
                return

    def add_check(self, check):
        SQL = ("INSERT INTO url_checks "
               "(url_id, status_code, h1, title, description, created_at) "
               "VALUES "
               "(%(url_id)s, %(status_code)s, %(h1)s, %(title)s, "
               "%(description)s, %(created_at)s) "
               "RETURNING id")

        with self.conn:
            self.make_sqlquery(SQL, check)

    def get_url_checks(self, id):
        SQL = ("SELECT * FROM url_checks "
               "WHERE url_id=%s ORDER BY created_at DESC")

        rows = self.make_sqlquery(SQL, (id,), fetch='all')
        return rows
