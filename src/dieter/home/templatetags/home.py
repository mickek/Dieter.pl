from django import template
from django.conf import settings

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