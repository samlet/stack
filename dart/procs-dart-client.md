# procs-dart-client.md
## start python multiplex server
```sh
start crmsfa
```

## start
```sh
## generate stubs
$ pub global activate protoc_plugin
$ cd crmsfa
$ ./gen-proto.sh

## build & run
$ pub get
$ dart bin/client.dart
```
