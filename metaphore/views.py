from django.template import loader
from django.views.generic.date_based import archive_index, archive_year, \
                        archive_month, archive_day, \
                        object_detail
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

from basemodels import Post

from taggit.models import TaggedItem


def metaphore_filters(request, queryset, extra_context,
                      content_type, tags, author):
    """ Filter the request based on certain parameters and add some info
        about the filters to the context. """

    if not queryset:
        queryset = Post.published_on_site.all()

    if not extra_context:
        extra_context = {}

    tags = request.GET.get('tags', tags)
    if tags:
        tag_list = tags.split(',')

        # As the objects that are tagged are actually the subclasses
        # of the post object, we'll have to go through some trouble to
        # get the related posts for a set of tags.

        # This might actually be a bug in django-taggit - WORK TO DO =)

        # First, figure out which are the subclasses we are interested in
        content_types = queryset.values_list('content_type', flat=True)
        content_types = content_types.distinct()

        # Second, find the tagged items relevant to our query
        tagged_items = \
            TaggedItem.objects.filter(content_type__id__in=content_types,
                                      tag__name__in=tag_list)

        # Blabla
        def tagged_to_post_id(obj):
            if obj.content_object:
                return obj.content_object.post_id

        # Make a list of pk's for relevant posts
        queryset = \
            queryset.filter(pk__in=map(tagged_to_post_id, tagged_items))

        # Later, when this bug is fixed - we might just be able to do it
        # like this:
        #queryset = queryset.filter(tag__name__in=tags)

        extra_context.update({'filter_tags': tags})

    content_type = request.GET.get('content_type', content_type)
    if content_type:
        ct = get_object_or_404(ContentType, model=content_type)
        queryset = queryset.filter(content_type=ct)

        extra_context.update({'filter_content_type': content_type})

    content_type = request.GET.get('author', content_type)
    if author:
        queryset = queryset.filter(author__username=author)

        extra_context.update({'filter_author': author})

    return queryset, extra_context


def metaphore_archive_index(request, queryset=None,
                date_field='publish_date', num_latest=15,
                template_name=None, template_loader=loader,
                extra_context=None, allow_empty=True,
                context_processors=None,
                mimetype=None, allow_future=False,
                template_object_name='object_list',
                content_type=None, tags=None,
                author=None):

    queryset, extra_context = metaphore_filters(request, queryset,
                                                extra_context,
                                                content_type, tags, author)


    return archive_index(request, queryset, date_field, num_latest,
                 template_name, template_loader,
                 extra_context, allow_empty, context_processors,
                 mimetype, allow_future, template_object_name)


def metaphore_archive_year(request, year, queryset=None,
               date_field='publish_date', template_name=None,
               template_loader=loader, extra_context=None,
               allow_empty=False, context_processors=None,
               template_object_name='object', mimetype=None,
               make_object_list=True, allow_future=False,
               content_type=None, tags=None, author=None):

    queryset, extra_context = metaphore_filters(request, queryset,
                                                extra_context,
                                                content_type, tags, author)


    return archive_year(request, year, queryset, date_field, template_name,
                template_loader, extra_context, allow_empty,
                context_processors, template_object_name, mimetype,
                make_object_list, allow_future)


def metaphore_archive_month(request, year, month, queryset=None,
                date_field='publish_date',
                month_format='%m', template_name=None,
                template_loader=loader, extra_context=None,
                allow_empty=False, context_processors=None,
                template_object_name='object', mimetype=None,
                allow_future=False, content_type=None, tags=None, 
                author=None):

    queryset, extra_context = metaphore_filters(request, queryset,
                                                extra_context,
                                                content_type, tags, author)


    return archive_month(request, year, month, queryset, date_field,
            month_format, template_name, template_loader,
            extra_context, allow_empty, context_processors,
            template_object_name, mimetype, allow_future)


def metaphore_archive_day(request, year, month, day, queryset=None,
              date_field='publish_date',
              month_format='%m', day_format='%d',
              template_name=None, template_loader=loader,
              extra_context=None, allow_empty=False,
              context_processors=None,
              template_object_name='object', mimetype=None,
              allow_future=False, content_type=None, tags=None, author=None):

    queryset, extra_context = metaphore_filters(request, queryset,
                                                extra_context,
                                                content_type, tags, author)


    return archive_day(request, year, month, day, queryset, date_field,
            month_format, day_format, template_name,
            template_loader, extra_context, allow_empty,
            context_processors, template_object_name,
            mimetype, allow_future)


def metaphore_object_detail(request, year, month, day, queryset=None,
                date_field='publish_date', month_format='%m',
                day_format='%d', object_id=None, slug=None,
                slug_field='slug', template_name=None,
                template_name_field=None, template_loader=loader,
                extra_context=None, context_processors=None,
                template_object_name='object', mimetype=None,
                allow_future=False, content_type=None, tags=None,
                author=None):

    queryset, extra_context = metaphore_filters(request, queryset,
                                                extra_context,
                                                content_type, tags, author)


    return object_detail(request, year, month, day, queryset, date_field,
            month_format, day_format, object_id, slug,
            slug_field, template_name, template_name_field,
            template_loader, extra_context, context_processors,
            template_object_name, mimetype, allow_future)
