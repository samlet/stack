def filter_term(s):
    return s.replace('"',"'").strip()

def lines(filename):
    with open(filename) as f:
        lines = f.readlines()
        return [line.split('\t') for line in lines]


# Yield successive n-sized
# chunks from l.
def divide_chunks(l, n):
    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n]

