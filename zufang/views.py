from django.shortcuts import render_to_response
from django.template import RequestContext

# Create your views here.

def zufang(request):
    return render_to_response('zufang_base.html', {
        }, context_instance=RequestContext(request))
