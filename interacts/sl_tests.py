import streamlit as st
# ⊕ [axiros/terminal_markdown_viewer: Styled Terminal Markdown Viewer](https://github.com/axiros/terminal_markdown_viewer#customization)
# ⊕ [terminal_markdown_viewer/mdv/tests/files at master · axiros/terminal_markdown_viewer](https://github.com/axiros/terminal_markdown_viewer/tree/master/mdv/tests/files)

st.markdown('''
### Source
# Header 1
## Header 2
### Header 3
#### Header 4
##### Header 5
###### Header 6
```python
""" Test """
# Make Py2 >>> Py3:
import os, sys; reload(sys); sys.setdefaultencoding('utf-8')
# no? see http://stackoverflow.com/a/29832646/4583360 ...

# code analysis for hilite:
try:
    from pygments import lex, token
    from pygments.lexers import get_lexer_by_name, guess_lexer
```

| Tables | Fmt |
| -- | -- |
| !!! hint: wrapped | 0.1 **strong** |

!!! note: title
    this is a Note
''')

st.markdown("""_
# Mdv installation

## Usage

    [sudo] ./setup.py install

----
""")

st.markdown('''
## Code Highlighting

Set -C <all|code|doc|mod> for source code highlighting of source code files.
Mark inline markdown with a '_' following the docstring beginnings.

- all: Show markdown docstrings AND code (default if you say, e.g. `-C.`)
- code: Only Code
- doc: Only docstrings with markdown
- mod: Only the module level docstring

## File Monitor:

If FROM is not found we display the whole file.

## Directory Monitor:

We check only text file changes, monitoring their size.

By default .md, .mdown, .markdown files are checked but you can change like `-M 'mydir:py,c,md,'` where the last empty substrings makes mdv also monitor any file w/o extension (like 'README').

### Running actions on changes:

If you append to `-M` a `'::<cmd>'` we run the command on any change detected (sync, in foreground).

The command can contain placeholders:

    _fp_     # Will be replaced with filepath
    _raw_    # Will be replaced with the base64 encoded raw content
               of the file
    _pretty_ # Will be replaced with the base64 encoded prettyfied output

Like: mdv -M './mydocs:py,md::open "_fp_"'  which calls the open
command with argument the path to the changed file.
''')

st.markdown("""
[link](http://foo.bar)
[link](http://foo.bar) this also

---

And [this](http://foo.com) is also [a](http://foo.bar) link

- And [this](http://foo.com) is also [a](http://foo.bar) link
- And [this](http://foo.com) is also [a](http://foo.bar) link

---

[link *with* **formatting** and `code`](http://foo.bar)
""")

st.markdown("""
> outer
>> inner

> long lnog long outer *em* [link](http://foo) end

>> inner *em* [link](http://foo) end

""")

st.markdown("""
* a `bar`
    * foo `bar`b
        * foo `bar`b
    * baz
* bazouter

""")

st.markdown("""
# Hello

Look at next code block.

```bash
command -stdin <<EOP
first line in stdin
second line in stdin
EOP
```

This is similar code block with ${variable} highlighted. But it looks broken.

    command -stdin ${variable} <<EOP
    first line in stdin
    second line in stdin
    EOP

It looks broken even if ${variable} present anywhere in code block.

    command -stdin <<EOP
    first line in stdin
    second line in stdin
    EOP

    ${variable}

Actually it works if code block contains ${variable} and <:

    First string <
    Second string with ${var}.
    Third string.

# The end.
""")