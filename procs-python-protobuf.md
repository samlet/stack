# procs-python-protobuf.md
⊕ [python - How to assign to repeated field? - Stack Overflow](https://stackoverflow.com/questions/23726335/how-to-assign-to-repeated-field)
    As per the documentation, you aren't able to directly assign to a repeated field. In this case, you can call extend to add all of the elements in the list to the field.
    person.id.extend([1, 32, 43432])

    If you don't want to extend but overwrite it completely, you can do:
    person.id[:] = [1, 32, 43432]
    This approach will also work to clear the field entirely:
    del person.id[:]

