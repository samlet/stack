# procs-networkx.md
⊕ [Tutorial — NetworkX 2.3rc1.dev20190113142240 documentation](https://networkx.github.io/documentation/latest/tutorial.html)

⊕ [Introduction — NetworkX 2.2 documentation](https://networkx.github.io/documentation/stable/reference/introduction.html#algorithms)

## algorithms
```python
# As an example here is code to use Dijkstra’s algorithm to find the shortest weighted path:

>>>
>>> G = nx.Graph()
>>> e = [('a', 'b', 0.3), ('b', 'c', 0.9), ('a', 'c', 0.5), ('c', 'd', 1.2)]
>>> G.add_weighted_edges_from(e)
>>> print(nx.dijkstra_path(G, 'a', 'd'))
['a', 'c', 'd']
```
