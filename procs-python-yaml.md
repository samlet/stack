# procs-python-yaml.md
⊕ [python - How can I write data in YAML format in a file? - Stack Overflow](https://stackoverflow.com/questions/12470665/how-can-i-write-data-in-yaml-format-in-a-file)
⊕ [Parse yaml into a list in python - Stack Overflow](https://stackoverflow.com/questions/32916092/parse-yaml-into-a-list-in-python)
⊕ [Basic Usage — Python YAML package documentation](https://yaml.readthedocs.io/en/latest/basicuse.html)

## start
```python
import yaml

data = dict(
    A = 'a',
    B = dict(
        C = 'c',
        D = 'd',
        E = 'e',
    )
)

with open('data.yml', 'w') as outfile:
    # yaml.dump(data, outfile, default_flow_style=False)
    yaml.dump(data, outfile)
```

+ save and load

```python
from ruamel.yaml import YAML
yaml = YAML()
with open('.services.yml', 'w') as outfile:
    yaml.dump(services, outfile)

# load
with open('.services.yml') as fp:
    str_data = fp.read()
data = yaml.load(str_data)
print(len(data), type(data))
print(data[:5])    
```

## more examples
⊕ [https://pyyaml.org/wiki/PyYAMLDocumentation](https://pyyaml.org/wiki/PyYAMLDocumentation)

```python
>>> documents = """
... ---
... name: The Set of Gauntlets 'Pauraegen'
... description: >
...     A set of handgear with sparks that crackle
...     across its knuckleguards.
... ---
... name: The Set of Gauntlets 'Paurnen'
... description: >
...   A set of gauntlets that gives off a foul,
...   acrid odour yet remains untarnished.
... ---
... name: The Set of Gauntlets 'Paurnimmen'
... description: >
...   A set of handgear, freezing with unnatural cold.
... """

>>> for data in yaml.load_all(documents):
...     print data

{'description': 'A set of handgear with sparks that crackle across its knuckleguards.\n',
'name': "The Set of Gauntlets 'Pauraegen'"}
{'description': 'A set of gauntlets that gives off a foul, acrid odour yet remains untarnished.\n',
'name': "The Set of Gauntlets 'Paurnen'"}
{'description': 'A set of handgear, freezing with unnatural cold.\n',
'name': "The Set of Gauntlets 'Paurnimmen'"}

>>> yaml.load("""
... none: [~, null]
... bool: [true, false, on, off]
... int: 42
... float: 3.14159
... list: [LITE, RES_ACID, SUS_DEXT]
... dict: {hp: 13, sp: 5}
... """)

{'none': [None, None], 'int': 42, 'float': 3.1415899999999999,
'list': ['LITE', 'RES_ACID', 'SUS_DEXT'], 'dict': {'hp': 13, 'sp': 5},
'bool': [True, False, True, False]}
```

### Constructors, representers, resolvers
You may define your own application-specific tags. The easiest way to do it is to define a subclass of yaml.YAMLObject:

```python
>>> class Monster(yaml.YAMLObject):
...     yaml_tag = u'!Monster'
...     def __init__(self, name, hp, ac, attacks):
...         self.name = name
...         self.hp = hp
...         self.ac = ac
...         self.attacks = attacks
...     def __repr__(self):
...         return "%s(name=%r, hp=%r, ac=%r, attacks=%r)" % (
...             self.__class__.__name__, self.name, self.hp, self.ac, self.attacks)

# The above definition is enough to automatically load and dump Monster objects:

>>> yaml.load("""
... --- !Monster
... name: Cave spider
... hp: [2,6]    # 2d6
... ac: 16
... attacks: [BITE, HURT]
... """)

Monster(name='Cave spider', hp=[2, 6], ac=16, attacks=['BITE', 'HURT'])

>>> print yaml.dump(Monster(
...     name='Cave lizard', hp=[3,6], ac=16, attacks=['BITE','HURT']))

!Monster
ac: 16
attacks: [BITE, HURT]
hp: [3, 6]
name: Cave lizard
```

## collections
```python
import yaml

inp='''
- state: idle
  status: 4
- state: running
  status: 4
- state: stopped

'''
yaml.load(inp)
```
```python
# Block mapping can be nested:

# YAML
hero:
  hp: 34
  sp: 8
  level: 4
orc:
  hp: 12
  sp: 0
  level: 2
# Python
{'hero': {'hp': 34, 'sp': 8, 'level': 4}, 'orc': {'hp': 12, 'sp': 0, 'level': 2}}
```

A block mapping may be nested in a block sequence:

```yaml
## YAML
- name: PyYAML
  status: 4
  license: MIT
  language: Python
- name: PySyck
  status: 5
  license: BSD
  language: Python
```
```python  
# Python
[{'status': 4, 'language': 'Python', 'name': 'PyYAML', 'license': 'MIT'},
{'status': 5, 'license': 'BSD', 'name': 'PySyck', 'language': 'Python'}]
```




