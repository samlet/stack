# procs-yaml.md
⊕ [parsing - How to parse/read a YAML file into a Python object? - Stack Overflow](https://stackoverflow.com/questions/6866600/how-to-parse-read-a-yaml-file-into-a-python-object)
⊕ [https://pyyaml.org/wiki/PyYAMLDocumentation](https://pyyaml.org/wiki/PyYAMLDocumentation)

## start            
```sh
pip install PyYAML
```
```yaml
# tree format
treeroot:
    branch1:
        name: Node 1
        branch1-1:
            name: Node 1-1
    branch2:
        name: Node 2
        branch2-1:
            name: Node 2-1
```
```python
import yaml
with open('tree.yaml') as f:
    # use safe_load instead load
    dataMap = yaml.safe_load(f)
    print(dataMap)
```

The yaml.dump function accepts a Python object and produces a YAML document.

```python
>>> print yaml.dump({'name': 'Silenthand Olleander', 'race': 'Human',
... 'traits': ['ONE_HAND', 'ONE_EYE']})

name: Silenthand Olleander
race: Human
traits: [ONE_HAND, ONE_EYE]
```
