# procs-gradle-mirror.md
** https://developer.aliyun.com/mvn/guide
在 build.gradle 文件中加入以下代码:

```js
allprojects {
  repositories {
    maven {
      url 'https://maven.aliyun.com/repository/public/'
    }
    mavenLocal()
    mavenCentral()
  }
}
```
```js
// 如果想使用其它代理仓，以使用spring仓为例，代码如下:

allProjects {
  repositories {
    maven {
      url 'https://maven.aliyun.com/repository/public/'
    }
    maven {
      url 'https://maven.aliyun.com/repository/spring/'
    }
    mavenLocal()
    mavenCentral()
  }
}
// 加入你要引用的文件信息：
dependencies {
  compile '[GROUP_ID]:[ARTIFACT_ID]:[VERSION]'
}
```

执行命令：

```sh
gradle dependencies # 或 ./gradlew dependencies 安装依赖
```

⊕ [gradle 使用 国内镜像 - 正义的伙伴！ - 博客园](https://www.cnblogs.com/whm-blog/p/12407786.html)

```js
// 在项目文件中找到build.gradle文件，修改其中的buildscript和allprojects地址：

buildscript {
    repositories {
        maven{ url 'http://maven.aliyun.com/nexus/content/groups/public/' }
        maven{ url 'http://maven.aliyun.com/nexus/content/repositories/jcenter'}
    }
    dependencies {
        classpath 'com.android.tools.build:gradle:3.3.0-alpha13'
    }
}

allprojects {
    repositories {
        maven{ url 'http://maven.aliyun.com/nexus/content/groups/public/'}
        maven{ url 'http://maven.aliyun.com/nexus/content/repositories/jcenter'}
    }
}
```

⊕ [Allow insecure protocols, android gradle - Stack Overflow](https://stackoverflow.com/questions/68585885/allow-insecure-protocols-android-gradle)
    allowInsecureProtocol = true

⊕ [阿里云maven镜像库配置（gradle,maven） - 迟到的月亮 - CSDN博客](https://blog.csdn.net/qq_32193151/article/details/70907037)

gradle配置：将原来的mavenCentral()直接替换掉或者放到这个的前面（默认是从上往下寻找，所以要放到mavenCentral的前面，如果加在mavenCentral后面，等同于没加）

```js
repositories {
    maven {url 'http://maven.aliyun.com/nexus/content/groups/public/'}
    mavenLocal()
    mavenCentral()
}
```

maven配置：

```xml
<repositories>
    <repository>
        <id>aliyunmaven</id>
        <url>http://maven.aliyun.com/nexus/content/groups/public/</url>
    </repository>
</repositories>
```
