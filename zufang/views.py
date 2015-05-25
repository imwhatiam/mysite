import logging

from django.shortcuts import render_to_response
from django.template import RequestContext

logger = logging.getLogger(__name__)
# Create your views here.

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def zufang(request):

    ip = get_client_ip(request)

    logger.info(ip)

    return render_to_response('zufang_base.html', {
        }, context_instance=RequestContext(request))
