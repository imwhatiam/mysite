# Create your views here.
import json
#import sqlite3
import socket, struct
import MySQLdb, MySQLdb.cursors

from functools import wraps
from rest_framework.views import APIView
from django.http import HttpResponse

from mysite.settings import MYSQL_INFO

JSON_CONTENT_TYPE = 'application/json; charset=utf-8'
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def ip2long(ip):
    """
    Convert an IP string to long
    """
    packedIP = socket.inet_aton(ip)
    return struct.unpack("!L", packedIP)[0]

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
            #con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("SELECT * FROM zufang ORDER BY timestamp DESC LIMIT 500")
            rows = cur.fetchall()

            for row in rows:
                item = {
                    'title': row["title"],
                    'url': row["url"],
                    'reply_time': row["reply_time"],
                }
                items.append(item)

        return items

class ZufangAccessCount(APIView):
    """
    Returns zufang access count.
    """
    @json_response
    def get(self, request, format=None):
        con = MySQLdb.connect(
                host = MYSQL_INFO['host'],
                port = 3306,
                user = MYSQL_INFO['user'],
                passwd = MYSQL_INFO['passwd'],
                db = 'mysite',
                charset = 'utf8',
                cursorclass = MySQLdb.cursors.DictCursor
            )

        ip = get_client_ip(request)
        with con:
            cur = con.cursor()

            cur.execute("SELECT times FROM zufang_access_count WHERE ip=%d" % ip2long(ip))
            my_times = cur.fetchone()

            cur.execute("SELECT SUM(times) FROM zufang_access_count;")
            total_times = cur.fetchone()

            cur.execute("SELECT COUNT(ip) FROM zufang_access_count;")
            total_visitors = cur.fetchone()

            item = {
                'ip': ip,
                'my_times': my_times['times'],
                'total_times': int(total_times['SUM(times)']),
                'total_visitors': int(total_visitors['COUNT(ip)']),
            }

        return item
