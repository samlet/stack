# procs-python-env.md
⊕ [1. Command line and environment — Python 3.7.2 documentation](https://docs.python.org/3/using/cmdline.html#envvar-PYTHONPATH)

+ When called with -m module-name, the given module is located on the Python module path and executed as a script.
    Search sys.path for the named module and execute its contents as the __main__ module.

    Many standard library modules contain code that is invoked on their execution as a script. An example is the timeit module:

    python -mtimeit -s 'setup here' 'benchmarked code here'
    python -mtimeit -h # for details

## Environment variables
+ https://docs.python.org/3/using/cmdline.html#environment-variables

PYTHONPATH: Augment the default search path for module files. The format is the same as the shell’s PATH: one or more directory pathnames separated by os.pathsep (e.g. colons on Unix or semicolons on Windows). Non-existent directories are silently ignored.

In addition to normal directories, individual PYTHONPATH entries may refer to zipfiles containing pure Python modules (in either source or compiled form). Extension modules cannot be imported from zipfiles.

The default search path is installation dependent, but generally begins with prefix/lib/pythonversion (see PYTHONHOME above). It is always appended to PYTHONPATH.

An additional directory will be inserted in the search path in front of PYTHONPATH as described above under Interface options. The search path can be manipulated from within a Python program as the variable sys.path.


