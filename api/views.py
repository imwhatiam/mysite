from rest_framework.views import APIView

from mysite.utils import get_client_ip, ip2long, json_response, \
        MySQLdb_con
from mysite.settings import MYSQL_INFO

class ZufangItems(APIView):
    """
    Returns all list.
    """
    @json_response
    def get(self, request, format=None):

        items = []
        con = MySQLdb_con()
        with con:
            cur = con.cursor()
            cur.execute(
                        "SELECT id, title, people_id, people_name, timestamp, reply_timestamp, reply_count\
                         FROM %s \
                         ORDER BY timestamp DESC LIMIT 500" % MYSQL_INFO['topic_table']
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
                    'content': '',
                }
                items.append(item)

        return items

class ZufangItem(APIView):
    """
    Returns all list.
    """
    @json_response
    def put(self, request, topic_id, format=None):
        pass

class ZufangAccessCount(APIView):
    """
    Returns zufang access count.
    """
    @json_response
    def get(self, request, format=None):

        ip = get_client_ip(request)
        ip_2_long = ip2long(ip)

        con = MySQLdb_con()
        with con:
            cur = con.cursor()

            cur.execute("SELECT times FROM %s WHERE ip=%d" %
                    (MYSQL_INFO['access_count_table'], ip_2_long))
            my_times = cur.fetchone()

            cur.execute("SELECT SUM(times) FROM %s;" %
                    MYSQL_INFO['access_count_table'])
            total_times = cur.fetchone()

            cur.execute("SELECT COUNT(ip) FROM %s;" %
                    MYSQL_INFO['access_count_table'])
            total_visitors = cur.fetchone()

            item = {
                'ip': ip,
                'my_times': my_times['times'],
                'total_times': int(total_times['SUM(times)']),
                'total_visitors': int(total_visitors['COUNT(ip)']),
            }

        return item

class ZufangSearchContent(APIView):
    """
    Returns zufang access count.
    """
    @json_response
    def get(self, request, format=None):

        value = request.GET.get('value')
        con = MySQLdb_con()
        items = []

        with con:
            cur = con.cursor()

            cur.execute("SELECT id, title, people_id, timestamp, content \
                         FROM %s \
                         WHERE title LIKE '%%%s%%' \
                         OR content LIKE '%%%s%%'" % (MYSQL_INFO['topic_info_table'], value, value)
                       )

            rows = cur.fetchall()

            for row in rows:
                item = {
                    'id': row["id"],
                    'topic_title': row["title"],
                    'people_id': row["people_id"],
                    'timestamp': row["timestamp"],
                    'content': row["content"],
                }
                items.append(item)

        return items
