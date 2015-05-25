import logging
import socket, struct
import MySQLdb, MySQLdb.cursors

from django.shortcuts import render_to_response
from django.template import RequestContext

from mysite.settings import MYSQL_INFO
logger = logging.getLogger(__name__)
# Create your views here.

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

def zufang(request):

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
        #con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("INSERT INTO zufang_access_count (ip, times) VALUES (%d, 1) ON DUPLICATE KEY UPDATE times=times+1; " % ip2long(ip))

    return render_to_response('zufang_base.html', {
        }, context_instance=RequestContext(request))
