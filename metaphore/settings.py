from django.conf import settings

OEMBED_MAX_WIDTH = getattr(settings, 'METAPHORE_OEMBED_MAX_WIDTH', None)
OEMBED_MAX_HEIGHT = getattr(settings, 'METAPHORE_OEMBED_MAX_HEIGHT', None)

USE_TINYMCE = getattr(settings, 'METAPHORE_USE_TINYMCE', False)

TAGS_REQUIRED = getattr(settings, 'METAPHORE_TAGS_REQUIRED', True)
