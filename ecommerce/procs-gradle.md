# procs-gradle.md
## gradle wrapper
⊕ [The Gradle Wrapper](https://docs.gradle.org/current/userguide/gradle_wrapper.html)

```bash
$ gradle wrapper --gradle-version 7.4.2 --distribution-type all
```

## ..
⊕ [Building Java Applications with libraries Sample](https://docs.gradle.org/current/samples/sample_building_java_applications_multi_project.html)

```bash
$ mkdir demo
$ cd demo
$ gradle init

Select type of project to generate:
  1: basic
  2: application
  3: library
  4: Gradle plugin
Enter selection (default: basic) [1..4] 2

Split functionality across multiple subprojects?:
   1: no - only one application project
   2: yes - application and library projects
Enter selection (default: no - only one application project) [1..2] 2

Select implementation language:
  1: C++
  2: Groovy
  3: Java
  4: Kotlin
  5: Scala
  6: Swift
Enter selection (default: Java) [1..6] 3

Select build script DSL:
  1: Groovy
  2: Kotlin
Enter selection (default: Groovy) [1..2] 1

Select test framework:
  1: JUnit 4
  2: TestNG
  3: Spock
  4: JUnit Jupiter
Enter selection (default: JUnit 4) [1..4]

Project name (default: demo):
Source package (default: demo):


BUILD SUCCESSFUL
2 actionable tasks: 2 executed
```
```ini
├── gradle 
│   └── wrapper
│       ├── gradle-wrapper.jar
│       └── gradle-wrapper.properties
├── gradlew 
├── gradlew.bat 
├── settings.gradle 
├── buildSrc
│   ├── build.gradle 
│   └── src
│       └── main
│           └── groovy 
│               ├── demo.java-application-conventions.gradle
│               ├── demo.java-common-conventions.gradle
│               └── demo.java-library-conventions.gradle
├── app
│   ├── build.gradle 
│   └── src
│       ├── main 
│       │   └── java
│       │       └── demo
│       │           └── app
│       │               ├── App.java
│       │               └── MessageUtils.java
│       └── test 
│           └── java
│               └── demo
│                   └── app
│                       └── MessageUtilsTest.java
├── list
│   ├── build.gradle 
│   └── src
│       ├── main 
│       │   └── java
│       │       └── demo
│       │           └── list
│       │               └── LinkedList.java
│       └── test 
│           └── java
│               └── demo
│                   └── list
│                       └── LinkedListTest.java
└── utilities
    ├── build.gradle 
    └── src
        └── main 
            └── java
                └── demo
                    └── utilities
                        ├── JoinUtils.java
                        ├── SplitUtils.java
                        └── StringUtils.java
```



⊕ [Declaring Dependencies between Subprojects](https://docs.gradle.org/current/userguide/declaring_dependencies_between_subprojects.html)

```js
dependencies {
    implementation project(':shared')
}
```

⊕ [java - Gradle application plugin with multiple main classes - Stack Overflow](https://stackoverflow.com/questions/43937169/gradle-application-plugin-with-multiple-main-classes/46938169)

```bash
# You can directly configure the Application Plugin with properties:
application {
    mainClassName = project.findProperty("chooseMain").toString()
}
# And after in command line you can pass the name of the main class:
./gradlew run -PchooseMain=net.worcade.my.MainClass
```

```js
pply plugin: 'java'

task(runSimple, dependsOn: 'classes', type: JavaExec) {
   main = 'com.mrhaki.java.Simple'
   classpath = sourceSets.main.runtimeClasspath
   args 'mrhaki'
   systemProperty 'simple.message', 'Hello '
}
```
Clearly then what you can change:
    runSimple can be named whatever you want
    set main as appropriate
    clear out args and systemProperty if not needed
    To run:

```bash
$ gradle runSimple
# If you want to pass arguments from the command line you can do this with: gradle runSimple --args 'arg1 arg2' (You'll need to remove the args bit from the task() obviously) 
```

⊕ [The Gradle Wrapper](https://docs.gradle.org/current/userguide/gradle_wrapper.html#sec:upgrading_wrapper)

## upgrade
```sh
$ ./gradlew wrapper --gradle-version 5.2.1
# $ ./gradlew wrapper --gradle-version 5.0 
# Checking the Wrapper version after upgrading
$ ./gradlew -v
```

## Project layout
⊕ [The Java Plugin](https://docs.gradle.org/current/userguide/java_plugin.html#resources)

The Java plugin assumes the project layout shown below. None of these directories need to exist or have anything in them. The Java plugin will compile whatever it finds, and handles anything which is missing.

    src/main/java
    Production Java source.

    src/main/resources
    Production resources, such as XML and properties files.

    src/test/java
    Test Java source.

    src/test/resources
    Test resources.

    src/sourceSet/java
    Java source for the source set named sourceSet.

    src/sourceSet/resources
    Resources for the source set named sourceSet.

## test
⊕ [Gradle build without tests - Stack Overflow](https://stackoverflow.com/questions/4597850/gradle-build-without-tests)

```sh
gradle build -x test 
```

## application
⊕ [Gradle to execute Java class (without modifying build.gradle) - Stack Overflow](https://stackoverflow.com/questions/21358466/gradle-to-execute-java-class-without-modifying-build-gradle)

You just need to use the Gradle Application plugin:

```js
apply plugin:'application'
mainClassName = "org.gradle.sample.Main"
```

And then simply gradle run.

As Teresa points out, you can also configure mainClassName as a system property and run with a command line argument.

@PaulVerest Here's what I did: 

```js
ext.mainClass = project.hasProperty('mainClass') ? project.getProperty('mainClass') : 'org.gradle.sample.Main' ; apply plugin:'application' ; mainClassName = ext.mainClass 
```
Now when you do gradle -PmainClass=Foo run it should use Foo as the main class.

