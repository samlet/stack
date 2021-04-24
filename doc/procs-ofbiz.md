# procs-ofbiz.md
⊕ [The Apache OFBiz® Project - Business Users](https://ofbiz.apache.org/business-users.html)
    .. Modules and Features
⊕ [OFBiz Tutorials | Get Started with Apache OFBiz Development](https://www.hotwaxsystems.com/ofbiz-8/tutorials/)
    ⊕ [What You Need to Know about Price Rules in OFBiz | HotWax](https://www.hotwaxsystems.com/ofbiz/ofbiz-tutorials/ofbiz-tutorial-price-rules/)

## framework
⊕ [SECAs and Error and Failure Management - OFBiz Project Open Wiki - Apache Software Foundation](https://cwiki.apache.org/confluence/display/OFBIZ/SECAs+and+Error+and+Failure+Management)
⊕ [Service Engine Guide - OFBiz Project Open Wiki - Apache Software Foundation](https://cwiki.apache.org/confluence/display/OFBIZ/Service+Engine+Guide#ServiceEngineGuide-ServiceEngineGuide-ecas)

## related projs
⊕ [OFBiz Migration | ScipioERP](https://www.scipioerp.com/community/developer/installation-configuration/ofbiz-migration/)
  ⊕ [ilscipio/scipio-erp: Your Online Business Kit - Build your own business applications. Create your own online shop. Customize to your own needs.](https://github.com/ilscipio/scipio-erp)

## build
```sh
./gradlew build
# 构建之后, build/distributions/ofbiz.zip中包含了ofbiz.jar以及所有依赖库, 其中bin下是执行脚本; build/libs/ofbiz.jar是ofbiz类;
```

+ gralde mirror (在allprojects.repositories下增加)

```js
allprojects {
    repositories{
        maven{ url 'http://maven.aliyun.com/nexus/content/groups/public/' }
        maven{ url 'http://maven.aliyun.com/nexus/content/repositories/jcenter'}
        ....
    }
}
```

## unit test
⊕ [From Ant to Gradle - trunk version - OFBiz Project Open Wiki - Apache Software Foundation](https://cwiki.apache.org/confluence/display/OFBIZ/From+Ant+to+Gradle+-+trunk+version#load-data-from-an-entity-file)

```sh
$ ./gradlew "ofbiz --test component=entity --test suitename=entitytests"
$ ./gradlew "ofbiz --test component=party -test name=party-tests"
```

## Business Process Reference
⊕ [Business Process Reference Book - OFBiz Project Open Wiki - Apache Software Foundation](https://cwiki.apache.org/confluence/display/OFBIZ/Business+Process+Reference+Book)

## rest
```sh
$ curl -k -X POST "https://localhost:8443/rest/auth/token" -H "accept: application/json" -H "Authorization: Basic YWRtaW46b2ZiaXo="
{
  "statusCode" : 200,
  "statusDescription" : "OK",
  "successMessage" : "Token granted.",
  "data" : {
    "access_token" : "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJ1c2VyTG9naW5JZCI6ImFkbWluIiwiaXNzIjoiQXBhY2hlT0ZCaXoiLCJleHAiOjE2MTIxNDIxODEsImlhdCI6MTYxMjE0MDM4MX0.qDll35GNzlzGobzNGpRpuP6GsJxdRDoOeJB-x9Ey2TBWsvtWz45izZAoYQ2M2DRDKnVJupn8kd-sUW-X6T8BAw",
    "token_type" : "Bearer",
    "expires_in" : "1800"
  }
}
```

+ Call OFBiz service via GET(export="true" and verb = "get|post")
    * https://localhost:8443/rest/services/findProductById?inParams=%7B%22idToFind%22:%22GZ-1001%22%7D

```ini
GET /rest/services/findProductById?inParams=%7B%22idToFind%22:%22GZ-1001%22%7D HTTP/1.1 +
Content-Type: application/json +
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJBcGFjaGVPRkJpeiIsImlhdCI6MTU0NzczOTM0OCwiZXhwIjoxNjc5Mjc1MzQ4LCJhdWQiOiJ3d3cuZXhhbXBsZS5jb20iLCJzdWIiOiJqcm9ja2V0QGV4YW1wbGUuY29tIiwiR2l2ZW5OYW1lIjoiSm9obm55IiwiU3VybmFtZSI6IlJvY2tldCIsIkVtYWlsIjoianJvY2tldEBleGFtcGxlLmNvbSIsInVzZXJMb2dpbklkIjoiYWRtaW4iLCJSb2xlIjpbIk1hbmFnZXIiLCJQcm9qZWN0IEFkbWluaXN0cmF0b3IiXX0.fwafgrgpodBJcXxNTQdZknKeWKb3sDOsQrcR2vcRw97FznD6mkE79p10Tu7cqpUx7LiXuROUAnXEgqDice-BSg
```

* 修改ModelServiceReader后用post方式访问: https://localhost:8443/rest/services/ping, bearer-token为前面获取的access_token, json内容需要是合法内容, 比如: {"x":"x"}
得到以下结果: 

```json
{
  "statusCode": 200,
  "statusDescription": "OK",
  "data": {
    "message": "PONG"
  }
}
```

+ 测试返回错误: https://localhost:8443/rest/services/testEntityFailure

```json
{
  "statusCode": 422,
  "statusDescription": "Unprocessable Entity",
  "errorType": "ServiceError",
  "errorMessage": "testEntityFailure returned error. The request contained invalid information and could not be processed.",
  "errorDescription": "Unable to create test entity"
}
```

+ 测试携带参数: https://localhost:8443/rest/services/testScv

```json
{
  "defaultValue":99.8,
  "message": "hello"
}

```
```json
{
  "statusCode": 200,
  "statusDescription": "OK",
  "data": {
    "resp": "service done"
  }
}
```

使用复合参数时: https://localhost:8443/rest/services/testScv
会被折叠成字符串到指定的参数中:

```json
{
  "defaultValue":99.8,
  "message": {
    "name":"hello"
  }
}
```
```ini
|I| ---- SVC-CONTEXT: message => {name=hello}
```

## debug
* 通过gradle/tasks/application/run上右击选择debug, 就可以进行断点调试;
    * 见: ofbiz-dev.docx

## plugins
⊕ [From Ant to Gradle - trunk version - OFBiz Project Open Wiki - Apache Software Foundation](https://cwiki.apache.org/confluence/display/OFBIZ/From+Ant+to+Gradle+-+trunk+version#FromAnttoGradletrunkversion-Step-by-stepguide)

```sh
# Create a new plugin
./gradlew createPlugin -PpluginId=myplugin
./gradlew createPlugin -PpluginId=myplugin -PpluginResourceName=MyPlugin -PwebappName=mypluginweb -PbasePermission=MYSECURITY
```

## postgres
⊕ [PostgreSQL: Documentation: 9.1: createuser](https://www.postgresql.org/docs/9.1/app-createuser.html)
⊕ [Creating user, database and adding access on PostgreSQL | by Arnav Gupta | Coding Blocks | Medium](https://medium.com/coding-blocks/creating-user-database-and-adding-access-on-postgresql-8bfcd2f4a91e)

```sh
# To create the user joe as a superuser, and assign a password immediately:

$ createuser -P -s -e ofbiz
# Enter password for new role: xyzzy
# Enter it again: xyzzy
# CREATE ROLE joe PASSWORD 'md5b5f5ba1a423792b526f799ae4eb3d59e' SUPERUSER CREATEDB CREATEROLE INHERIT LOGIN;

$ createdb ofbiz
$ psql ofbiz
# psql=# grant all privileges on database <dbname> to <username> ;
ofbiz=# grant all privileges on database ofbiz to ofbiz;
```

## auth
* 可修改token的expireTime:
    * ofbiz-rest-impl/src/main/java/org/apache/ofbiz/ws/rs/resources/AuthenticationResource.java
    * framework/security/config/security.properties
        @Path("/token")
        .. EntityUtilProperties.getPropertyValue("security", "security.jwt.token.expireTime", "1800", getDelegator())

```bash
# 18000000/60/60 = 5000.0小时 = 208.3天
curl -k -X POST "https://localhost:8443/rest/auth/token" -H "accept: application/json" -H "Authorization: Basic YWRtaW46b2ZiaXo="
{
  "statusCode" : 200,
  "statusDescription" : "OK",
  "successMessage" : "Token granted.",
  "data" : {
    "access_token" : "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJ1c2VyTG9naW5JZCI6ImFkbWluIiwiaXNzIjoiQXBhY2hlT0ZCaXoiLCJleHAiOjE2MzQ1OTc3NTcsImlhdCI6MTYxNjU5Nzc1N30.Luuf2bK7ZJ8KE_CtsA3iPZ189i-Qbm2qK5r5VfeQcJqIyTKy4DHf2fBAp37W8OtU6SIplwCdnbTMtHuCZ5h8cA",
    "token_type" : "Bearer",
    "expires_in" : "18000000"
  }
}
```


