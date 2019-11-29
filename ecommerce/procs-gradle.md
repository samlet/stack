# procs-gradle.md
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

