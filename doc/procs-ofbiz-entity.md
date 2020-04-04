# procs-ofbiz-entity.md
## not null (pk字段非空)
```java
if (field.getIsNotNull() || field.getIsPk()) {
    if (this.datasourceInfo.getAlwaysUseConstraintKeyword()) {
        sqlBuf.append(" CONSTRAINT NOT NULL, ");
    } else {
        sqlBuf.append(" NOT NULL, ");
    }
} else {
    sqlBuf.append(", ");
}
```


