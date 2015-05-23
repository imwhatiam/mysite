# Create your views here.
import json
import sqlite3
import MySQLdb, MySQLdb.cursors

from functools import wraps
from rest_framework.views import APIView
from django.http import HttpResponse

from mysite.settings import MYSQL_INFO

JSON_CONTENT_TYPE = 'application/json; charset=utf-8'
def json_response(func):
    @wraps(func)
    def wrapped(*a, **kw):
        result = func(*a, **kw)
        if isinstance(result, HttpResponse):
            return result
        else:
            return HttpResponse(json.dumps(result), status=200,
                                content_type=JSON_CONTENT_TYPE)
    return wrapped

class ZufangItems(APIView):
    """
    Returns all list.
    """
    @json_response
    def get(self, request, format=None):

        items = []
        #con = sqlite3.connect('/home/lian/zufang.db')
        con = MySQLdb.connect(
                host = MYSQL_INFO['host'],
                port = 3306,
                user = MYSQL_INFO['user'],
                passwd = MYSQL_INFO['passwd'],
                db = 'mysite',
                charset = 'utf8',
                cursorclass = MySQLdb.cursors.DictCursor
            )

        with con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("SELECT * FROM zufang ORDER BY timestamp DESC LIMIT 250")
            rows = cur.fetchall()

            for row in rows:
                item = {
                    'title': row["title"],
                    'url': row["url"],
                    'reply_time': row["reply_time"],
                }
                items.append(item)

        return items
