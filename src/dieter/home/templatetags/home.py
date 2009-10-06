from django import template
from django.conf import settings
from django.template import resolve_variable
from django.contrib.auth.models import Group


register = template.Library()

@register.simple_tag
def google_analytics_code():
    if settings.DEBUG:
        return ""
    else:
        return """
<script type="text/javascript">
var gaJsHost = (("https:" == document.location.protocol) ? "https://ssl." : "http://www.");
document.write(unescape("%%3Cscript src='" + gaJsHost + "google-analytics.com/ga.js' type='text/javascript'%%3E%%3C/script%%3E"));
</script>
<script type="text/javascript">
try {
var pageTracker = _gat._getTracker("%s");
pageTracker._trackPageview();
} catch(err) {}</script>""" % settings.GOOGLE_ANALYTICS_ID

@register.simple_tag
def jquery():
    
    uncompressed = 'false'
    if True: 
        return """<script src="%sjs/jquery-1.3.2.js"></script>
<script src="%sjs/jquery-ui-1.7.2.js"></script>
<script src="%sjs/jquery.ui.datepicker-pl.js"></script>""" % (settings.MEDIA_URL, settings.MEDIA_URL, settings.MEDIA_URL)
    else:
        return """<script src="http://www.google.com/jsapi"></script>
<script type="text/javascript">
google.load("jquery", "1.3.2",{uncompressed:%s});
google.load("jqueryui", "1.7.1",{uncompressed:%s});
<script src="%sjs/jquery.ui.datepicker-pl.js"></script>
</script>""" % (uncompressed, uncompressed, settings.MEDIA_URL)


@register.tag()
def ifusergroup(parser, token):
    """ Check to see if the currently logged in user belongs to a specific
    group. Requires the Django authentication contrib app and middleware.

    Usage: {% ifusergroup Admins %} ... {% endifusergroup %}

    """
    try:
        tag, group = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("Tag 'ifusergroup' requires 1 argument.")
    nodelist = parser.parse(('endifusergroup',))
    parser.delete_first_token()
    return GroupCheckNode(group, nodelist)


class GroupCheckNode(template.Node):
    def __init__(self, group, nodelist):
        self.group = group
        self.nodelist = nodelist
    def render(self, context):
        user = resolve_variable('user', context)
        if not user.is_authenticated:
            return ''
        try:
            group = Group.objects.get(name=self.group)
        except Group.DoesNotExist: #@UndefinedVariable
            return ''
        if group in user.groups.all():
            return self.nodelist.render(context)
        return ''