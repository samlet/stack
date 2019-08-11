# procs-rocksdb-java.md
⊕ [RocksJava Basics · facebook/rocksdb Wiki](https://github.com/facebook/rocksdb/wiki/RocksJava-Basics)

## start
```xml
<dependency>
  <groupId>org.rocksdb</groupId>
  <artifactId>rocksdbjni</artifactId>
  <version>5.5.1</version>
</dependency>
```

```java
import org.rocksdb.RocksDB;
import org.rocksdb.Options;
...
  // a static method that loads the RocksDB C++ library.
  RocksDB.loadLibrary();

  // the Options class contains a set of configurable DB options
  // that determines the behaviour of the database.
  try (final Options options = new Options().setCreateIfMissing(true)) {
    
    // a factory method that returns a RocksDB instance
    try (final RocksDB db = RocksDB.open(options, "path/to/db")) {
    
        // do something
    }
  } catch (RocksDBException e) {
    // do some error handling
    ...
  }
...
```

