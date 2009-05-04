from hyphen import hyphenator, dictools

from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

from django import template
register = template.Library()

from django.conf import settings

@register.filter
def hyphenate(value, arg=None, autoescape=None):
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x
    
    if arg:
        args = arg.split(u',')
        code = args[0]
        if len(args) > 1:
            minlen = int(args[1])
        else:
            minlen = 5
    else:
        code = settings.LANGUAGE_CODE
    s = code.split(u'-')
    lang = s[0].lower() + u'_' + s[1].upper()
    
    if not dictools.is_installed(lang): 
        dictools.install(lang)
        
    h = hyphenator(lang)
    new = []
    for word in value.split(u' '):
        if len(word) > minlen and word.isalpha():
            new.append(u'&shy;'.join(h.syllables(word)))
        else:
            new.append(word)
    
    result = u' '.join(new)
    return mark_safe(result)
hyphenate.needs_autoescape = True
    

    
