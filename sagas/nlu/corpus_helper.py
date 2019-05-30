def filter_term(s):
    return s.replace('"',"'").strip()

def lines(filename):
    with open(filename) as f:
        lines = f.readlines()
        return [line.split('\t') for line in lines]

