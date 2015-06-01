import socket, struct
import json
import MySQLdb, MySQLdb.cursors

from functools import wraps
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

def MySQLdb_con():
    con = MySQLdb.connect(
            host = MYSQL_INFO['host'],
            port = 3306,
            user = MYSQL_INFO['user'],
            passwd = MYSQL_INFO['passwd'],
            db = 'mysite',
            charset = 'utf8',
            cursorclass = MySQLdb.cursors.DictCursor
        )
    return con
