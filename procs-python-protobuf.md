# procs-python-protobuf.md
⊕ [Protocol Buffer Basics: Python  |  Protocol Buffers  |  Google Developers](https://developers.google.com/protocol-buffers/docs/pythontutorial)
⊕ [python - How to assign to repeated field? - Stack Overflow](https://stackoverflow.com/questions/23726335/how-to-assign-to-repeated-field)
    As per the documentation, you aren't able to directly assign to a repeated field. In this case, you can call extend to add all of the elements in the list to the field.
    person.id.extend([1, 32, 43432])

    If you don't want to extend but overwrite it completely, you can do:
    person.id[:] = [1, 32, 43432]
    This approach will also work to clear the field entirely:
    del person.id[:]

## start
```python
from simple_pb2 import MyObj, Foo
obj=MyObj(name='hello')
print(obj)

message = Foo()
message.name = "Bender"
assert message.HasField("name")
message.serial_number = 2716057
assert message.HasField("serial_number")
assert not message.HasField("name")
message.ClearField("test_oneof")

assert message.WhichOneof("test_oneof") is None
message.name = "Bender"
assert message.WhichOneof("test_oneof") == "name"

## 
import nlpserv_pb2 as nlp_messages
import nlpserv_pb2_grpc as nlp_service
p = nlp_messages.NlTokenizerRequest(text=nlp_messages.NlText(text="这里是北京"))
# response = client.Tokenizer(request)
result=nlp_procs(p, lambda stub, p: stub.Tokenizer(p))
for resp in result.tokens:
    print(resp.text)
```

## collection
```protobuf
message GetUsersRequest {
  repeated User user = 1;
}
```
```python
request = users_messages.GetUsersRequest(
        user=[users_messages.User(username="alexa", user_id=1),
              users_messages.User(username="christie", user_id=1)]
    )

## extend a collection
mapping = MetaFieldMapping(...)
package[key] = MetaFieldMappings(fields=[mapping])
...
package[key].fields.extend([mapping])
...
```

## parse
⊕ [Protocol Buffer Basics: Python  |  Protocol Buffers  |  Google Developers](https://developers.google.com/protocol-buffers/docs/pythontutorial)

```python
#! /usr/bin/python

import addressbook_pb2
import sys

# This function fills in a Person message based on user input.
def PromptForAddress(person):
  person.id = int(raw_input("Enter person ID number: "))
  person.name = raw_input("Enter name: ")

  email = raw_input("Enter email address (blank for none): ")
  if email != "":
    person.email = email

  while True:
    number = raw_input("Enter a phone number (or leave blank to finish): ")
    if number == "":
      break

    phone_number = person.phones.add()
    phone_number.number = number

    type = raw_input("Is this a mobile, home, or work phone? ")
    if type == "mobile":
      phone_number.type = addressbook_pb2.Person.MOBILE
    elif type == "home":
      phone_number.type = addressbook_pb2.Person.HOME
    elif type == "work":
      phone_number.type = addressbook_pb2.Person.WORK
    else:
      print "Unknown phone type; leaving as default value."

# Main procedure:  Reads the entire address book from a file,
#   adds one person based on user input, then writes it back out to the same
#   file.
if len(sys.argv) != 2:
  print "Usage:", sys.argv[0], "ADDRESS_BOOK_FILE"
  sys.exit(-1)

address_book = addressbook_pb2.AddressBook()

# Read the existing address book.
try:
  f = open(sys.argv[1], "rb")
  address_book.ParseFromString(f.read())
  f.close()
except IOError:
  print sys.argv[1] + ": Could not open file.  Creating a new one."

# Add an address.
PromptForAddress(address_book.people.add())

# Write the new address book back to disk.
f = open(sys.argv[1], "wb")
f.write(address_book.SerializeToString())
f.close()
```


