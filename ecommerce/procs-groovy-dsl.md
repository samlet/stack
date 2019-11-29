# procs-groovy-dsl.md
⊕ [Groovy DSLS](https://www.tutorialspoint.com/groovy/groovy_dsls.htm)
⊕ [Domain-Specific Languages](http://docs.groovy-lang.org/docs/latest/html/documentation/core-domain-specific-languages.html)

## start
```js
show = { println it }
square_root = { Math.sqrt(it) }

def please(action) {
  [the: { what ->
    [of: { n -> action(what(n)) }]
  }]
}

// equivalent to: please(show).the(square_root).of(100)
please show the square_root of 100
// ==> 10.0
```
