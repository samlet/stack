import sys
import urwid

class DialogExit(Exception):
    pass


class DialogDisplay:
    palette = [
        ('body','black','light gray', 'standout'),
        ('border','black','dark blue'),
        ('shadow','white','black'),
        ('selectable','black', 'dark cyan'),
        ('focus','white','dark blue','bold'),
        ('focustext','light gray','dark blue'),
        ]

    def __init__(self, text, height, width, body=None):
        width = int(width)
        if width <= 0:
            width = ('relative', 80)
        height = int(height)
        if height <= 0:
            height = ('relative', 80)

        self.body = body
        if body is None:
            # fill space with nothing
            body = urwid.Filler(urwid.Divider(),'top')

        self.frame = urwid.Frame( body, focus_part='footer')
        if text is not None:
            self.frame.header = urwid.Pile( [urwid.Text(text),
                urwid.Divider()] )
        w = self.frame

        # pad area around listbox
        w = urwid.Padding(w, ('fixed left',2), ('fixed right',2))
        w = urwid.Filler(w, ('fixed top',1), ('fixed bottom',1))
        w = urwid.AttrWrap(w, 'body')

        # "shadow" effect
        w = urwid.Columns( [w,('fixed', 2, urwid.AttrWrap(
            urwid.Filler(urwid.Text(('border','  ')), "top")
            ,'shadow'))])
        w = urwid.Frame( w, footer =
            urwid.AttrWrap(urwid.Text(('border','  ')),'shadow'))

        # outermost border area
        w = urwid.Padding(w, 'center', width )
        w = urwid.Filler(w, 'middle', height )
        w = urwid.AttrWrap( w, 'border' )

        self.view = w


    def add_buttons(self, buttons):
        l = []
        for name, exitcode in buttons:
            b = urwid.Button( name, self.button_press )
            b.exitcode = exitcode
            b = urwid.AttrWrap( b, 'selectable','focus' )
            l.append( b )
        self.buttons = urwid.GridFlow(l, 10, 3, 1, 'center')
        self.frame.footer = urwid.Pile( [ urwid.Divider(),
            self.buttons ], focus_item = 1)

    def button_press(self, button):
        raise DialogExit(button.exitcode)

    def main(self):
        self.loop = urwid.MainLoop(self.view, self.palette)
        try:
            self.loop.run()
        except DialogExit as e:
            return self.on_exit( e.args[0] )

    def on_exit(self, exitcode):
        return exitcode, ""

class ListDialogDisplay(DialogDisplay):
    def __init__(self, text, height, width, constr, items, has_default=False):
        j = []
        if has_default:
            k, tail = 3, ()
        else:
            k, tail = 2, ("no",)
        while items:
            j.append( items[:k] + tail )
            items = items[k:]

        l = []
        self.items = []
        for tag, item, default in j:
            w = constr( tag, default=="on" )
            self.items.append(w)
            w = urwid.Columns( [('fixed', 12, w),
                urwid.Text(item)], 2 )
            w = urwid.AttrWrap(w, 'selectable','focus')
            l.append(w)

        lb = urwid.ListBox(urwid.SimpleListWalker(l))
        lb = urwid.AttrWrap( lb, "selectable" )
        DialogDisplay.__init__(self, text, height, width, lb )

        self.frame.set_focus('body')

    def unhandled_key(self, size, k):
        if k in ('up','page up'):
            self.frame.set_focus('body')
        if k in ('down','page down'):
            self.frame.set_focus('footer')
        if k == 'enter':
            # pass enter to the "ok" button
            self.frame.set_focus('footer')
            self.buttons.set_focus(0)
            self.view.keypress( size, k )

    def on_exit(self, exitcode):
        """Print the tag of the item selected."""
        if exitcode != 0:
            return exitcode, ""
        s = ""
        for i in self.items:
            if i.get_state():
                s = i.get_label()
                break
        return exitcode, s

def run_it(d):
    exitcode, exitstring = d.main()
    # Exit
    if exitstring:
        sys.stderr.write(exitstring + "\n")

    sys.exit(exitcode)

class UrwidProcs(object):
    def do_msgbox(self, text, height=0, width=0):
        d = DialogDisplay( text, height, width )
        d.add_buttons([    ("OK", 0) ])
        # Run it
        run_it(d)

    def do_grid(self, text, height=0, width=0):
        """
        $ python -m sagas.tests.cli.urwid_procs do_grid hello
        :param text:
        :param height:
        :param width:
        :return:
        """
        def constr(tag, state):
            return urwid.CheckBox(tag, state)
        d = ListDialogDisplay( text, height, width, constr,
                               ('first', 'second', 'third', 'fourth') )

        d.add_buttons([    ("OK", 0) ])
        # Run it
        run_it(d)

if __name__ == '__main__':
    import fire
    fire.Fire(UrwidProcs)
