# procs-ofbiz-java-routines.md
+ json
    ⊕ [java - Convert Map to JSON using Jackson - Stack Overflow](https://stackoverflow.com/questions/29340383/convert-map-to-json-using-jackson)

```java
// You can convert Map to JSON using Jackson as follows:

Map<String,String> payload = new HashMap<>();
payload.put("key1","value1");
payload.put("key2","value2");

String json = new ObjectMapper().writeValueAsString(payload);
System.out.println(json);
```

