# procs-python-functions.md
⊕ [4. Map, Filter and Reduce — Python Tips 0.1 documentation](http://book.pythontips.com/en/latest/map_filter.html)

```python
items = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x**2, items))

def multiply(x):
    return (x*x)
def add(x):
    return (x+x)

funcs = [multiply, add]
for i in range(5):
    value = list(map(lambda x: x(i), funcs))
    print(value)

# Output:
# [0, 0]
# [1, 2]
# [4, 4]
# [9, 6]
# [16, 8]
```

