# procs-groovy.md
⊕ [Creating New Gradle Builds](https://guides.gradle.org/creating-new-gradle-builds/)
⊕ [Gradle Build a Groovy Project](https://www.tutorialspoint.com/gradle/gradle_build_a_groovy_project.htm)

## xml
⊕ [Groovy XML](https://www.tutorialspoint.com/groovy/groovy_xml.htm)

## start
```sh
❯ mkdir basic-demo
❯ cd basic-demo
❯ gradle init 
```
The Groovy plugin assumes a certain setup of your Groovy project.

src/main/groovy contains the Groovy source code
src/test/groovy contains the Groovy tests
src/main/java contains the Java source code
src/test/java contains the Java tests

```sh
$ mkdir -p src/main/groovy
$ mkdir -p src/test/groovy
$ mkdir -p src/main/java
$ mkdir -p src/test/java
```

+ build.gradle file.

```java
apply plugin: 'groovy'

repositories {
   mavenCentral()
}

dependencies {
   compile 'org.codehaus.groovy:groovy-all:2.4.5'
   testCompile 'junit:junit:4.12'
}
```

```sh
./gradlew build
```


