import logging
import datetime

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.cache import cache
from django.http import HttpResponse

from mysite.utils import get_client_ip, ip2long, MySQLdb_con
from mysite.settings import MYSQL_INFO

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

    return render_to_response('zufang_base.html',  context_instance=RequestContext(request))

def write_xls(sheet_name, head, data_list):
    """write listed data into excel
    """

    try:
        import xlwt
    except ImportError as e:
        logger.error(e)
        return None

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet(sheet_name)

    # prepare table head
    head_style = xlwt.XFStyle()
    head_style.font.bold = True
    row_num = 0

    # write table head
    for col_num in xrange(len(head)):
        ws.write(row_num, col_num, head[col_num], head_style)

    # write table data
    for row in data_list:
        row_num += 1
        for col_num in xrange(len(row)):
            ws.write(row_num, col_num, row[col_num])

    return wb

def export_excel(request):

    head = [
        "topic",
        "douban link",
        "author",
        "create time",
        "reply",
        "last reply",
        "content",
    ]

    data_list = []
    items = cache.get('zufang_items_excle')
    if not items:
        items = []
        con = MySQLdb_con()
        with con:
            cur = con.cursor()
            cur.execute(
                        "SELECT id, title, people_id, people_name, timestamp, reply_timestamp, reply_count, content\
                         FROM %s \
                         ORDER BY timestamp DESC LIMIT 2500" % MYSQL_INFO['topic_table']
                       )

            rows = cur.fetchall()

            for row in rows:
                item = {
                    'id': row["id"],
                    'title': row["title"],
                    'people_id': row["people_id"],
                    'people_name': row["people_name"],
                    'timestamp': row["timestamp"],
                    'reply_timestamp': row["reply_timestamp"],
                    'reply_count': row["reply_count"],
                    'content': row["content"],
                }
                items.append(item)

        cache.set('zufang_items_excle', items, 6 * 30 * 30)

    for item in items:
        excel_row = [item['title'],
                "http://www.douban.com/group/topic/" + str(item['id']) + "/",
                item['people_name'],
                datetime.datetime.fromtimestamp(item['timestamp']).strftime('%Y-%m-%d %H:%M'),
                item['reply_count'],
                datetime.datetime.fromtimestamp(item['reply_timestamp']).strftime('%Y-%m-%d %H:%M'),
                item['content'],
            ]

        data_list.append(excel_row)

    wb = write_xls('zufang', head, data_list)

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=zufang.xls'
    wb.save(response)

    return response
