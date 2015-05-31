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

            cur.execute("SELECT a.id, a.title, a.reply_time, a.timestamp, a.likes, b.user_id, b.user_name \
                FROM %s a, %s b \
                WHERE a.id = b.topic_id \
                ORDER BY a.timestamp DESC LIMIT 500" %
                (MYSQL_INFO['topic_table'], MYSQL_INFO['user_table']))

            rows = cur.fetchall()

            for row in rows:
                item = {
                    'id': row["id"],
                    'topic_title': row["title"],
                    'reply_time': row["reply_time"],
                    'user_id': row["user_id"],
                    'user_name': row["user_name"],
                    'likes': int(row['likes']),
                }
                items.append(item)

        return items

class ZufangItem(APIView):
    """
    Returns all list.
    """
    @json_response
    def put(self, request, topic_id, format=None):

        ip = get_client_ip(request)

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
            cur = con.cursor()
            ip = int(ip2long(ip))

            cur.execute("SELECT COUNT(ip) FROM zufang_topic_like where id=%d;" % int(topic_id))
            ver = cur.fetchone()
            result = {
                'likes': int(ver['COUNT(ip)']),
            }

            cur.execute("SELECT COUNT(*) FROM zufang_topic_like where id=%d AND ip=%d;" % (int(topic_id), ip))
            ver = cur.fetchone()
            if int(ver['COUNT(*)']) > 0:
                result['like_success'] = False
            else:
                cur.execute("INSERT INTO %s (%s, %s) VALUES (%d, %d)" % ('zufang_topic_like', 'id', 'ip', int(topic_id), ip))

                result['like_success'] = True
                result['likes'] = result['likes'] + 1

            cur.execute("UPDATE %s SET likes=%d WHERE id=%d" % ('zufang_topic', result['likes'], int(topic_id)))
        return result

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
