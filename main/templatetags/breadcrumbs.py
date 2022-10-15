from django import template

register = template.Library()


@register.simple_tag
def breadcrumbs(*args):
    results = []
    for i in args:
        i = i.split(',')
        try:
            results.append(
                {'name': i[0], 'url': i[1], 'active': bool(int(i[-1]))}
            )
        except IndexError:
            pass
    return results
