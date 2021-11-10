# procs-groovy-projects.md
⊕ [java - Require Gradle project from another directory - Stack Overflow](https://stackoverflow.com/questions/19299316/require-gradle-project-from-another-directory)
⊕ [配置子项目 · Gradle 实战](https://lippiouyang.gitbooks.io/gradle-in-action-cn/content/multi-project/configure-subproject.html)
    .. 你可以用allprojects方法给所有的项目添加group和version属性，由于根项目不需要Java插件，你可以使用subprojects给所有子项目添加Java插件

```js
allprojects {
    group = 'com.manning.gia'
    version = '0.1'
}

subprojects {
    apply plugin: 'java'
}
```

⊕ [gradle的ext属性 - 简书](https://www.jianshu.com/p/207c9f6f68c2)
    .. 用ext属性，和直接在build.gradle中用def定义变量的好处是什么？
    ext属性可以伴随对应的ExtensionAware对象在构建的过程中被其他对象访问，例如你在rootProject中声明的ext中添加的内容，就可以在任何能获取到rootProject的地方访问这些属性，而如果只在rootProject/build.gradle中用def来声明这些变量，那么这些变量除了在这个文件里面访问之外，其他任何地方都没办法访问。

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

