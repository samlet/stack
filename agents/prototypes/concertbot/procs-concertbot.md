# procs-concertbot.md
## start
```sh
## chinese_hanlp dir: duckling
$ run

## stack dir
$ start actions

## concertbot dir
$ make run-core

$ start greet
[{"recipient_id":"default","text":"hey there!"}]

$ start search_venues
[{"recipient_id":"default","text":"here are some venues I found"},{"recipient_id":"default","text":"Big Arena, Rock Cellar"}]

### 启动中文nlu的支持
$ make run-core-nlu
$ start search_venues_s
[{"recipient_id":"default","text":"here are some venues I found"},{"recipient_id":"default","text":"Big Arena, Rock Cellar"}]
```

## nlu-ch support
```sh
## chinese_hanlp dir
$ ./train.sh 
$ ./nlu-server.sh 
```


