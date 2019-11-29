# procs-gradle-tasks.md
⊕ [java - gradle - copy file after its generation - Stack Overflow](https://stackoverflow.com/questions/30636905/gradle-copy-file-after-its-generation)

## copy jar
I think the above answer is somehow old. Here is an answer using gradle 3.3

```js
jar {
    baseName = 'my-app-name'
    version =  '0.0.1'
}

task copyJar(type: Copy) {
    from jar // here it automatically reads jar file produced from jar task
    into 'destination-folder'
}

build.dependsOn copyJar
```

