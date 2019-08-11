# procs-dgraph-routines.md
## schema-mutation-query
```python
import sagas.graph.dgraph_helper as helper
import pydgraph
client=helper.reset('name: string @index(term) @lang .')
# or
client = helper.create_client()

helper.set_nquads(client, '''
    _:x1 <name> "名字1"@zh .
    _:x2 <name> "名字2"@zh .
''')

helper.run_q(client, '''{
   q(func: anyofterms(name@., "<名字1 名字2>")) {
     name@.
   }
}''')
```

## Password type
A password for an entity is set with setting the schema for the attribute to be of type password. Passwords cannot be queried directly, only checked for a match using the checkpwd function. The passwords are encrypted using bcrypt.

For example: to set a password, first set schema, then the password:

```ini
pass: password .
```
```js
{
  set {
    <0x123> <name> "Password Example" .
    <0x123> <pass> "ThePassword" .
  }
}
```
+ to check a password:

```js
{
  check(func: uid(0x123)) {
    name
    checkpwd(pass, "ThePassword")
  }
}
```
+ output:

```json
{
  "data": {
    "check": [
      {
        "name": "Password Example",
        "checkpwd(pass)": true
      }
    ]
  }
}
```
+ You can also use alias with password type.

```js
{
  check(func: uid(0x123)) {
    name
    secret: checkpwd(pass, "ThePassword")
  }
}
```
```json
{
  "data": {
    "check": [
      {
        "name": "Password Example",
        "secret": true
      }
    ]
  }
}
```


