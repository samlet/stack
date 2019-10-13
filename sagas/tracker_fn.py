from sagas.runtime import runtime

info=lambda *args, sep=' ', end='\n', file=None: runtime.tracker.info(*args)
emp=lambda c, *args: runtime.tracker.emphasis(c, *args)
label=lambda l, *args: runtime.tracker.label_text(l, *args)

dfs=lambda *args: runtime.tracker.dfs(*args)
gv=lambda v: runtime.tracker.gv(v)

# import sagas.tracker_fn as tc
# tc.info(...)

