# procs-aio-pika.md
+ workspace/python-aio/aio-pika
⊕ [mosquito/aio-pika: Wrapper for the PIKA for asyncio and humans.](https://github.com/mosquito/aio-pika)

## install
```sh
$ pip install aio-pika==4.8.0
# issue: 默认安装的是5.1版本, rpc-client/server工作不正常, 可能是因为:
# Since version 5.0.0 this library doesn't use pika as AMQP connector. Versions below 5.0.0 contains or requires pika's source codes.
```
+ rabbit docker

```sh
# NOTE: In order to run the tests locally you need to run a RabbitMQ instance with default user/password (guest/guest) and port (5672).
docker run -d -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```
