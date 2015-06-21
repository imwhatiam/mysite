import logging

from django.shortcuts import render_to_response
from django.template import RequestContext

from mysite.utils import get_client_ip, ip2long, MySQLdb_con
from mysite.settings import MYSQL_INFO, NOTICE

logger = logging.getLogger(__name__)

# Create your views here.

def zufang(request):

    ip = get_client_ip(request)
    ip_2_long = ip2long(ip)

    con = MySQLdb_con()
    with con:
        #con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("INSERT INTO %s (ip, times) VALUES (%d, 1) ON DUPLICATE KEY UPDATE times=times+1; " %
                (MYSQL_INFO['access_count_table'], ip_2_long))

    return render_to_response('zufang_base.html', {'notice': NOTICE
        }, context_instance=RequestContext(request))

def zufang_jyjx(request):

    return render_to_response('zufang_jyjx.html', {}, context_instance=RequestContext(request))
