def quote_str(val):
    val=val.strip()
    if val.endswith(','):
        val = val[0:-1]

    if val.startswith("'"):
        val='"'+val[1:-1]+'"'
    elif val.startswith('"'):
        pass
    else:
        val='"'+val+'"'
    return val

class Clips(object):
    def fmt_paras(self):
        """
        $ python -m sagas.shortcuts.clips fmt_paras
        :param input_text:
        :return:
        """
        import clipboard
        input_text = clipboard.paste()
        rs=[]
        for line in input_text.splitlines():
            line = line.strip()
            parts = line.split(':')
            if parts[0]!="userLogin":
                rs.append(f'{quote_str(parts[0])}: {quote_str(parts[1])},')
        for r in rs:
            print(r)
        clipboard.copy('\n'.join(rs))

if __name__ == '__main__':
    import fire
    fire.Fire(Clips)
