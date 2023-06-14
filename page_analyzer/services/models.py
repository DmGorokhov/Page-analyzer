import psycopg2
from psycopg2.extras import DictCursor
from datetime import datetime


class DBSession:

    def __init__(self, db_url):
        self.conn = psycopg2.connect(db_url)

    def make_sqlquery(self, sql, data=None, fetch=None):
        with self.conn:
            with self.conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(sql, data)
                sql_response = None
                match fetch:
                    case 'one':
                        sql_response = cursor.fetchone()
                    case 'all':
                        sql_response = cursor.fetchall()
                return sql_response

    def close(self):
        self.conn.close()


class DBUrlsModel:

    def __init__(self, db_conn):
        self.db_conn = db_conn

    def get_url(self, id):
        SQL = f"SELECT * FROM urls WHERE id={id}"
        row = self.db_conn.make_sqlquery(SQL, fetch='one')
        return row

    def find_url(self, url):
        SQL = 'SELECT id FROM urls WHERE name LIKE %s'
        url_id = self.db_conn.make_sqlquery(SQL, (url,), fetch='one')
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

        rows = self.db_conn.make_sqlquery(SQL, fetch='all')
        return rows

    def add_url(self, url):
        SQL = ("INSERT INTO urls (name, created_at) "
               "VALUES (%s, %s) RETURNING id")

        data = (url, datetime.now())
        added_id = self.db_conn.make_sqlquery(SQL, data, fetch='one')[0]
        return added_id

    def add_check(self, check):
        SQL = ("INSERT INTO url_checks "
               "(url_id, status_code, h1, title, description, created_at) "
               "VALUES "
               "(%(url_id)s, %(status_code)s, %(h1)s, %(title)s, "
               "%(description)s, %(created_at)s) "
               "RETURNING id")

        self.db_conn.make_sqlquery(SQL, check)

    def get_url_checks(self, id):
        SQL = ("SELECT * FROM url_checks "
               "WHERE url_id=%s ORDER BY created_at DESC")

        rows = self.db_conn.make_sqlquery(SQL, (id,), fetch='all')
        return rows
