from django.template import loader
from django.views.generic.date_based import archive_index, archive_year, archive_month, archive_day, object_detail
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

from basemodels import Post

def metaphore_archive_index(request, queryset=None, date_field='publish_date', num_latest=15,
        template_name=None, template_loader=loader,
        extra_context=None, allow_empty=True, context_processors=None,
        mimetype=None, allow_future=False, template_object_name='object_list', content_type=None):
        
        if not queryset:
            queryset = Post.published_on_site.all()

        if content_type:
            ct = get_object_or_404(ContentType, name=content_type)
            queryset.filter(content_type=ct)
        
        return archive_index(request, queryset, date_field, num_latest,
                        template_name, template_loader,
                        extra_context, allow_empty, context_processors,
                        mimetype, allow_future, template_object_name)

def metaphore_archive_year(request, year, queryset=None, date_field='publish_date', template_name=None,
        template_loader=loader, extra_context=None, allow_empty=False,
        context_processors=None, template_object_name='object', mimetype=None,
        make_object_list=True, allow_future=False, content_type=None):

        if not queryset:
            queryset = Post.published_on_site.all()

        if content_type:
            ct = get_object_or_404(ContentType, name=content_type)
            queryset.filter(content_type=ct)
        
        return archive_year(request, year, queryset, date_field, template_name,
                        template_loader, extra_context, allow_empty,
                        context_processors, template_object_name, mimetype,
                        make_object_list, allow_future)

def metaphore_archive_month(request, year, month, queryset=None, date_field='publish_date',
        month_format='%m', template_name=None, template_loader=loader,
        extra_context=None, allow_empty=False, context_processors=None,
        template_object_name='object', mimetype=None, allow_future=False, content_type=None):

        if not queryset:
            queryset = Post.published_on_site.all()

        if content_type:
            ct = get_object_or_404(ContentType, name=content_type)
            queryset.filter(content_type=ct)
        
        return archive_month(request, year, month, queryset, date_field,
                        month_format, template_name, template_loader,
                        extra_context, allow_empty, context_processors,
                        template_object_name, mimetype, allow_future)

def metaphore_archive_day(request, year, month, day, queryset=None, date_field='publish_date',
        month_format='%m', day_format='%d', template_name=None,
        template_loader=loader, extra_context=None, allow_empty=False,
        context_processors=None, template_object_name='object',
        mimetype=None, allow_future=False, content_type=None):
        
        if not queryset:
            queryset = Post.published_on_site.all()

        if content_type:
            ct = get_object_or_404(ContentType, name=content_type)
            queryset.filter(content_type=ct)

        return archive_day(request, year, month, day, queryset, date_field,
                        month_format, day_format, template_name,
                        template_loader, extra_context, allow_empty,
                        context_processors, template_object_name,
                        mimetype, allow_future)

def metaphore_object_detail(request, year, month, day, queryset=None, date_field='publish_date',
        month_format='%m', day_format='%d', object_id=None, slug=None,
        slug_field='slug', template_name=None, template_name_field=None,
        template_loader=loader, extra_context=None, context_processors=None,
        template_object_name='object', mimetype=None, allow_future=False, content_type=None):

        if not queryset:
            queryset = Post.published_on_site.all()

        if content_type:
            ct = get_object_or_404(ContentType, name=content_type)
            queryset.filter(content_type=ct)
        
        return object_detail(request, year, month, day, queryset, date_field,
                        month_format, day_format, object_id, slug,
                        slug_field, template_name, template_name_field,
                        template_loader, extra_context, context_processors,
                        template_object_name, mimetype, allow_future)