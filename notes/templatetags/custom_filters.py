from django import template
from django.utils.html import strip_tags
import html
import re

register = template.Library()

@register.filter
def strip_tags_and_truncate(value, num_words=None):
    """
    Custom filter to strip HTML tags, decode HTML entities, and truncate text
    to 'num_words', while preserving readable spaces. If 'num_words' is None,
    it will return the full content.
    """
    value = html.unescape(value)
    value = strip_tags(value)
    value = re.sub(r'<br\s*/?>', ' ', value)
    value = re.sub(r'\s+', ' ', value).strip()
    words = value.split(' ')
    if num_words is None:
        return value
    try:
        num_words = int(num_words)
    except ValueError:
        return value

    truncated_value = ' '.join(words[:num_words])
    if len(words) > num_words:
        truncated_value += '...'
    return truncated_value