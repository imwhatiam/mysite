from django.shortcuts import render_to_response
from django.template import RequestContext

# Create your views here.

def todos(request):
    return render_to_response('todos/index.html', {
        }, context_instance=RequestContext(request))
