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
${_('The')} fuzzy ${ungettext('bunny', 'bunnies', random.randint(1, 2))}

