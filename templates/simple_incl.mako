## -*- coding:utf-8 -*-
<%namespace file="funcs.mako" import="*"/>
<%!
import re
import mylib

def filter(text):
    text=gettext(text)
    return re.sub(r'^@', '', text)
%>
${myfunc(7)}
${mylib.welcome()}
