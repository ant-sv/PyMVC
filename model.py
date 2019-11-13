from psycopg2 import connect, ProgrammingError
from feedparser import parse
from datetime import datetime

class Model:

    DB_VERS = None
    _conn = None
    _curs = None
    start = None
    end = None

    def __init__(self):
        self.DB_CONF = 'dbname=test user=test host=localhost password=test'
        self.conn_error = self.connect_db()
        self.urls = {
            'all':         'https://habrahabr.ru/rss/all/all/',
            'best':        'https://habrahabr.ru/rss/best/',
            'best_week':   'https://habrahabr.ru/rss/best/weekly/',
            'best_month':  'https://habrahabr.ru/rss/best/monthly/',
            'interesting': 'https://habrahabr.ru/rss/interesting/',
            'hubs':        'https://habrahabr.ru/rss/hubs/all/'
        }

    def __del__(self):
        if self._conn:
            self._conn.close()
        if self._curs:
            self._curs.close()

    def connect_db(self):
        try:
            self._conn = connect(self.DB_CONF)
        except Exception as e:
            return e
        else:
            self._curs = self._conn.cursor()
            result = self.request_db("""SELECT VERSION();""")
            if type(result) is ProgrammingError:
                return result
            self.DB_VERS = result[0][0]
            self.request_db("""CREATE TABLE IF NOT EXISTS habr_data (
                id TEXT PRIMARY KEY,
                title TEXT,
                author TEXT,
                published TIMESTAMPTZ,
                tags TEXT[]);""")
            return self._conn.closed

    def update_data(self):
        data = self.request_rss()
        if not data:
            return 0
        for row in data:
            query = """INSERT INTO habr_data (id, title, author, published, tags)
                                VALUES (%s, %s, %s, %s, %s)
                                ON CONFLICT (id) DO NOTHING;"""
            params = (row[0], row[1], row[2], (row[3],), (row[4],))
            self.request_db(query, params)
        return 1

    def request_rss(self):
        data = []
        for _, value in self.urls.items():
            current = parse(value)
            for item in current.entries:
                row = list()
                row.append(item.id)
                row.append(item.title)
                row.append(item.author)
                dt = datetime.strptime(item.published, "%a, %d %b %Y %H:%M:%S %Z")
                row.append(dt)
                tags_list = list()
                for tag in item.tags:
                    tags_list.append(tag.term)
                row.append(tags_list)
                data.append(row)
        return data

    def get_tags(self):
        query = """SELECT DISTINCT LOWER(unnest)
            FROM (SELECT unnest(tags) FROM habr_data) AS all_tags
            ORDER BY LOWER(unnest);"""
        result = self.request_db(query)
        return result

    def top_tags(self):
        query = """SELECT LOWER(unnest), count(*)
            FROM (SELECT unnest(tags) FROM habr_data) AS all_tags
            GROUP BY LOWER(unnest)
            ORDER BY count DESC
            LIMIT 10;"""
        result = self.request_db(query)
        return result

    def top_authors(self):
        query = """SELECT author, count(*)
            FROM habr_data
            GROUP BY author
            ORDER BY count DESC
            LIMIT 10;"""
        result = self.request_db(query)
        return result

    @staticmethod
    def convert_date(string):
        try:
            date = datetime.date(datetime.strptime(string, "%d-%m-%y"))
        except ValueError as e:
            return e
        else:
            return date

    def check_wrong_tag(self, tag):
        query = """SELECT unnest
            FROM (SELECT unnest(tags) FROM habr_data) AS all_tags
            WHERE LOWER(unnest) = LOWER(%s);"""
        params = (tag,)
        result = self.request_db(query, params)
        return result

    def get_articles_week(self):
        query = """SELECT *
            FROM habr_data
            WHERE published > %s - '1 week'::interval;"""
        params = (datetime.now(),)
        result = self.request_db(query, params)
        return result

    def find_articles(self, tag, start, end):
        if start > end:
            self.start, self.end = end, start
        else:
            self.start, self.end = start, end
        query = """SELECT * FROM habr_data
            WHERE %s ilike ANY(tags)
            AND (published between %s AND %s + '1 day'::interval);"""
        params = (tag, self.start, self.end)
        result = self.request_db(query, params)
        return result

    def request_db(self, query, params=None):
        try:
            result = None
            self._curs.execute(query, params)
            if self._curs.description:
                result = self._curs.fetchall()
        except Exception as e:
            print(e)
            self._conn.rollback()
            return e
        else:
            self._conn.commit()
            return result
