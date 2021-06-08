# procs-gradle.md
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

