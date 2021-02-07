# procs-ofbiz.md
⊕ [The Apache OFBiz® Project - Business Users](https://ofbiz.apache.org/business-users.html)
    .. Modules and Features
⊕ [OFBiz Tutorials | Get Started with Apache OFBiz Development](https://www.hotwaxsystems.com/ofbiz-8/tutorials/)
    ⊕ [What You Need to Know about Price Rules in OFBiz | HotWax](https://www.hotwaxsystems.com/ofbiz/ofbiz-tutorials/ofbiz-tutorial-price-rules/)

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

