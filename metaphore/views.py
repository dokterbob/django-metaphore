# from django.shortcuts import render_to_response, get_object_or_404
# from django.core.paginator import Paginator, InvalidPage, EmptyPage
# from django.template import RequestContext
# from menu.models import Menu
# from models import *
# 
# 
# 
# def home(request):
#     # logic here
#     return render_to_response('home.html', RequestContext(request, c))
# 
# 
# def foto_list(request):
#     # logic here
#     objects = Photo.objects.all()
#     paginate_by = 12
#     paginator = Paginator(objects, paginate_by)
# 
#     # Make sure page request is an int. If not, deliver first page.
#     try:
#         page = int(request.GET.get('page', '1'))
#     except ValueError:
#         page = 1
# 
#     # If page request (9999) is out of range, deliver last page of results.
#     try:
#         objects = paginator.page(page)
#     except (EmptyPage, InvalidPage):
#         objects = paginator.page(paginator.num_pages)
#     
#     c = {'objects'    : objects }
#     return render_to_response('foto_list.html', RequestContext(request, c))

from django.template import loader
from django.views.generic.date_based import archive_index, archive_year, archive_month, archive_day, object_detail
from basemodels import Post

def metaphore_archive_index(request, queryset=None, date_field='publish_date', num_latest=15,
        template_name=None, template_loader=loader,
        extra_context=None, allow_empty=True, context_processors=None,
        mimetype=None, allow_future=False, template_object_name='object_list'):
        
        if not queryset:
            queryset = Post.published_on_site.all()
        
        return archive_index(request, queryset, date_field, num_latest,
                        template_name, template_loader,
                        extra_context, allow_empty, context_processors,
                        mimetype, allow_future, template_object_name)

def metaphore_archive_year(request, year, queryset=None, date_field='publish_date', template_name=None,
        template_loader=loader, extra_context=None, allow_empty=False,
        context_processors=None, template_object_name='object', mimetype=None,
        make_object_list=True, allow_future=False):

        if not queryset:
            queryset = Post.published_on_site.all()
        
        return archive_year(request, year, queryset, date_field, template_name,
                        template_loader, extra_context, allow_empty,
                        context_processors, template_object_name, mimetype,
                        make_object_list, allow_future)

def metaphore_archive_month(request, year, month, queryset=None, date_field='publish_date',
        month_format='%m', template_name=None, template_loader=loader,
        extra_context=None, allow_empty=False, context_processors=None,
        template_object_name='object', mimetype=None, allow_future=False):

        if not queryset:
            queryset = Post.published_on_site.all()
        
        return archive_month(request, year, month, queryset, date_field,
                        month_format, template_name, template_loader,
                        extra_context, allow_empty, context_processors,
                        template_object_name, mimetype, allow_future)

def metaphore_archive_day(request, year, month, day, queryset=None, date_field='publish_date',
        month_format='%m', day_format='%d', template_name=None,
        template_loader=loader, extra_context=None, allow_empty=False,
        context_processors=None, template_object_name='object',
        mimetype=None, allow_future=False):
        
        if not queryset:
            queryset = Post.published_on_site.all()

        return archive_day(request, year, month, day, queryset, date_field,
                        month_format, day_format, template_name,
                        template_loader, extra_context, allow_empty,
                        context_processors, template_object_name,
                        mimetype, allow_future)

def metaphore_object_detail(request, year, month, day, queryset=None, date_field='publish_date',
        month_format='%m', day_format='%d', object_id=None, slug=None,
        slug_field='slug', template_name=None, template_name_field=None,
        template_loader=loader, extra_context=None, context_processors=None,
        template_object_name='object', mimetype=None, allow_future=False):

        if not queryset:
            queryset = Post.published_on_site.all()
        
        return object_detail(request, year, month, day, queryset, date_field,
                        month_format, day_format, object_id, slug,
                        slug_field, template_name, template_name_field,
                        template_loader, extra_context, context_processors,
                        template_object_name, mimetype, allow_future)