<%!
import random
def gettext(message): return message
_ = gettext
def ungettext(s, p, c):
    if c == 1:
        return s
    return p
top = gettext('Begin')
%>
<%def name="myfunc(x)">
this is myfunc, x is ${x}
</%def>
