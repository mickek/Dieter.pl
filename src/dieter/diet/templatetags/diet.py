from django import template

register = template.Library()

def meals_section(context, type, name, meals):
    return { 'MEDIA_URL':context['MEDIA_URL'], 'meals': meals, 'name': name, 'type': type}

register.inclusion_tag('diet/meals_section.html', takes_context=True)(meals_section)