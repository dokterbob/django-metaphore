from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.template import RequestContext
from menu.models import Menu
from models import *

def home(request):
    # logic here
    return render_to_response('home.html', RequestContext(request, c))


def foto_list(request):
    # logic here
    objects = Photo.objects.all()
    paginate_by = 12
    paginator = Paginator(objects, paginate_by)

    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # If page request (9999) is out of range, deliver last page of results.
    try:
        objects = paginator.page(page)
    except (EmptyPage, InvalidPage):
        objects = paginator.page(paginator.num_pages)
    
    c = {'objects'    : objects }
    return render_to_response('foto_list.html', RequestContext(request, c))

