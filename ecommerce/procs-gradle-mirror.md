# procs-gradle-mirror.md
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
