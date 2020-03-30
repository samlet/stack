def write_proto_to(proto, file):
    from os.path import expanduser
    with open(expanduser(file), "wb") as f:
        f.write(proto.SerializeToString())

def read_proto(proto, file):
    from os.path import expanduser
    with open(expanduser(file), "rb") as f:
        proto.ParseFromString(f.read())

def convert_proto(java_proto, py_proto):
    form_data = java_proto.toByteString().toByteArray()
    py_proto.ParseFromString(form_data)
    return py_proto

