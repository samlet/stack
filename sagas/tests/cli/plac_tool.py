from datetime import datetime

# ⊕ [plac.rst](http://micheles.github.io/plac/)

def main(dsn, table='product', today=datetime.today()):
    "Do something on the database"
    print(dsn, table, today)

if __name__ == '__main__':
    """
    ⊕ [plac · PyPI](https://pypi.org/project/plac/)
    $ python sagas/tests/cli/plac_tool.py -h
    """
    import plac; plac.call(main)

