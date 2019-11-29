# procs-groovy-projects.md
⊕ [java - Require Gradle project from another directory - Stack Overflow](https://stackoverflow.com/questions/19299316/require-gradle-project-from-another-directory)

## require-gradle-project-from-another-directory
The simplest way is to make MyProject a multi project with the Logger project as a subproject.

settings.gradle in MyProject directory:

```js
include ":logger"
project(":logger").projectDir = file("../logger")
```
In the build.gradle of MyProject you can now reference this lib as a project:

```java
dependencies {
     compile 'com.android.support:gridlayout-v7:18.0.0'
     compile 'com.android.support:appcompat-v7:18.0.0'
     compile project(":logger")
}
```

