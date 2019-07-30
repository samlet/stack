# ⊕ [Convert a list to a dictionary in Python - Stack Overflow](https://stackoverflow.com/questions/4576115/convert-a-list-to-a-dictionary-in-python)
def to_dict(a):
    i = iter(a)
    b = dict(zip(i, i))
    return b

convert_list=lambda a: {a[i]: a[i+1] for i in range(0, len(a), 2)}
convert_list_to_seq_dict=lambda listOfStr: { i : listOfStr[i] for i in range(0, len(listOfStr) ) }
convert_2_list=lambda a1,a2: dict(zip(a1, a2))


