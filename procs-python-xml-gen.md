# procs-python-xml-gen.md
⊕ [Yattag - Download and install](http://www.yattag.org/download-install)
⊕ [Yattag - Generate HTML with Python](http://www.yattag.org/)

## start
```sh
pip install yattag
```

## issues
⊕ [Current API does not allow attributes with "-" in name (as "data-..." attribute) · Issue #3 · leforestier/yattag](https://github.com/leforestier/yattag/issues/3)
    
    New release 1.0.4: you can now pass attributes as (key, value) pairs to the tag and stag method.

    with tag('simple-method', ("result-name", "x")):
        # doc.attr(("result-name", "x"))

        