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

            cur.execute("SELECT a.id, a.title, a.timestamp, a.likes, b.id, b.user_name \
                         FROM %s a, %s b \
                         WHERE a.id = b.topic_id \
                         ORDER BY a.timestamp DESC LIMIT 500" %
                (MYSQL_INFO['topic_table'], MYSQL_INFO['user_table']))

            rows = cur.fetchall()

            for row in rows:
                item = {
                    'id': row["id"],
                    'topic_title': row["title"],
                    'timestamp': row["timestamp"],
                    'user_id': row["id"],
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

        topic_id = int(topic_id)

        ip = get_client_ip(request)
        ip_2_long = ip2long(ip)

        con = MySQLdb_con()
        with con:
            cur = con.cursor()

            cur.execute("SELECT COUNT(ip) FROM %s where id=%d;" %
                    (MYSQL_INFO['topic_like_table'], topic_id))
            row = cur.fetchone()
            result = {
                'likes': int(row['COUNT(ip)']),
            }

            cur.execute("SELECT COUNT(*) FROM %s where id=%d AND ip=%d;" %
                    (MYSQL_INFO['topic_like_table'], topic_id, ip_2_long))
            row = cur.fetchone()

            if int(row['COUNT(*)']) > 0:
                result['like_success'] = False
            else:
                cur.execute("INSERT INTO %s VALUES (%d, %d)" %
                        (MYSQL_INFO['topic_like_table'], topic_id, ip_2_long))

                result['like_success'] = True
                result['likes'] = result['likes'] + 1

            cur.execute("UPDATE %s SET likes=%d WHERE id=%d" %
                    (MYSQL_INFO['topic_table'], result['likes'], topic_id))

        return result

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
                    'timestamp': row["timestamp"],
                    'content': row["content"],
                }
                items.append(item)

        return items
