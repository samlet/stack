# procs-dgraph.md
⊕ [dgraph-io/dgraph: Fast, Distributed Graph DB](https://github.com/dgraph-io/dgraph)
⊕ [Clients — Dgraph Doc v1.0.14](https://docs.dgraph.io/clients/)
⊕ [pydgraph/README.md at master · dgraph-io/pydgraph](https://github.com/dgraph-io/pydgraph/blob/master/README.md)
⊕ [Dgraph-查询语言 - 简书](https://www.jianshu.com/p/d9ffe5a57779)
⊕ [A Tour of Dgraph](https://tour.dgraph.io/)

⊕ [Get started — Dgraph Doc v1.0.14](https://docs.dgraph.io/get-started/)
⊕ [Dgraph 1.0.12 发布，事务性的分布式图形数据库 - OSCHINA](https://www.oschina.net/news/104959/dgraph-1-0-12-released)
⊕ [Dgraph概念 - 简书](https://www.jianshu.com/p/db730cbf282f)
⊕ [Dgraph事务详解 - 简书](https://www.jianshu.com/p/c0b047589aac?from=timeline)
⊕ [Dgraph-Take a tour - 简书](https://www.jianshu.com/p/63760573d2cf)

⊕ [Neo4j vs Dgraph - 这些数字不言自明--Dgraph博客](https://blog.dgraph.io/post/benchmark-neo4j/)
  .. 我们仅为每个请求使用了20个并发连接和200个N-Quads，因为如果我们增加连接数或每个连接的N-Quads，Neo4j就不能正常工作。事实上，这是使Neo4j数据损坏并挂起系统3.2的可靠方法。对于Dgraph，我们通常每个请求发送1000个N-Quads并且具有500个并发连接。
  .. 凭借110万N-Quads的黄金数据集，Dgraph的 表现优于Neo4j 46.7k至280 N-Quads/秒。事实上，Neo4j加载程序从未完成（我们在相当长的等待之后将其杀死）。 对于加载图形数据，Dgraph比Neo4j快160倍。


## docker
⊕ [dgraph/dgraph - Docker Hub](https://hub.docker.com/r/dgraph/dgraph)
    Dgraph is at version 1.0.0 and is production ready.
    - latest 63 MB Last update: 20 days ago
    - v1.0.14 63 MB Last update: 20 days ago
    + https://github.com/dgraph-io/dgraph/blob/master/contrib/Dockerfile

## start
```sh
# stack/compose/dev/docker-compose.yml
start dev
open http://localhost:8000/
```

## mutate
```js
{
  set {
   _:luke <name> "Luke Skywalker" .
   _:leia <name> "Princess Leia" .
   _:han <name> "Han Solo" .
   _:lucas <name> "George Lucas" .
   _:irvin <name> "Irvin Kernshner" .
   _:richard <name> "Richard Marquand" .

   _:sw1 <name> "Star Wars: Episode IV - A New Hope" .
   _:sw1 <release_date> "1977-05-25" .
   _:sw1 <revenue> "775000000" .
   _:sw1 <running_time> "121" .
   _:sw1 <starring> _:luke .
   _:sw1 <starring> _:leia .
   _:sw1 <starring> _:han .
   _:sw1 <director> _:lucas .

   _:sw2 <name> "Star Wars: Episode V - The Empire Strikes Back" .
   _:sw2 <release_date> "1980-05-21" .
   _:sw2 <revenue> "534000000" .
   _:sw2 <running_time> "124" .
   _:sw2 <starring> _:luke .
   _:sw2 <starring> _:leia .
   _:sw2 <starring> _:han .
   _:sw2 <director> _:irvin .

   _:sw3 <name> "Star Wars: Episode VI - Return of the Jedi" .
   _:sw3 <release_date> "1983-05-25" .
   _:sw3 <revenue> "572000000" .
   _:sw3 <running_time> "131" .
   _:sw3 <starring> _:luke .
   _:sw3 <starring> _:leia .
   _:sw3 <starring> _:han .
   _:sw3 <director> _:richard .

   _:st1 <name> "Star Trek: The Motion Picture" .
   _:st1 <release_date> "1979-12-07" .
   _:st1 <revenue> "139000000" .
   _:st1 <running_time> "132" .
  }
}
```

## 一些问题的整理
+ multiple databases? 
⊕ [Does DGraph support multiple databases? - Users - Discuss Dgraph](https://discuss.dgraph.io/t/does-dgraph-support-multiple-databases/2714/2)
    Exactly. Graph databases were designed to eliminate the use of tables as in SQL. So it would not make much sense to return to this logic, you know? Graph DB’s are another paradigm.

+ multiple schema
⊕ [Is there any demo written for multiple schema - Users - Discuss Dgraph](https://discuss.dgraph.io/t/is-there-any-demo-written-for-multiple-schema/2180/2)
⊕ [Can't understand doc section "giving nodes a type" - Users - Discuss Dgraph](https://discuss.dgraph.io/t/cant-understand-doc-section-giving-nodes-a-type/2266/2)
⊕ [Howto — Dgraph Doc v1.0.14](https://docs.dgraph.io/howto/#giving-nodes-a-type)

这里的想法是，如果你有一个独特的谓词，你期望一个类型的所有节点都有它，它是最好的。
例如，假设Person类型的所有节点都可以拥有person_name。然后，您可以通过has(person_name)在root上执行查询来获取所有类型为person的节点。同样地，假设您有一个订单，并且您知道所有订单必须与某些订单相关，order_items那么这将成为定义订单的唯一谓词。Type由于文档中提到的原因，这比在所有节点上具有优势更好。

好的，我知道了。这是一种鸭子打字。“如果它的行为=像鸭子一样具有谓词，它就是一只鸭子”
与谓词命名约定相结合，_:Pawan <person.name> "Pawan" .现在对我来说很有意义。
找到所有人： has(person.name)

## 新增、修改数据和uid引用
⊕ [dgraph中schema的阅读笔记 - zuxiaoyuan - 博客园](https://www.cnblogs.com/zuxiaoyuan/p/9285199.html)

dgraph为每个数据节点创建它自己的内部的id，但是我们有时我们需要多次使用一个节点，就像下面例子中的_:company1一样：

```js
{
set {
_:company1 <name> "CompanyABC" .
_:company2 <name> "The other company" .

_:company1 <industry> "Machinery" .

_:company2 <industry> "High Tech" .

_:jack <works_for> _:company1 .
_:ivy <works_for> _:company1 .
_:zoe <works_for> _:company1 .

_:jose <works_for> _:company2 .
_:alexei <works_for> _:company2 .

_:ivy <boss_of> _:jack .

_:alexei <boss_of> _:jose .
}
}
```
//运行结果如下：

```json
{
  "data": {
    "code": "Success",
    "message": "Done",
    "uids": {
      "alexei": "0x21",
      "company1": "0x22",
      "company2": "0x23",
      "ivy": "0x25",
      "jack": "0x24",
      "jose": "0x20",
      "zoe": "0x1f"
    }
  },
  "extensions": {
    "server_latency": {
      "parsing_ns": 330152,
      "processing_ns": 8271549
    },
    "txn": {
      "start_ts": 86,
      "commit_ts": 87,
      "lin_read": {
        "ids": {
          "1": 65
        }
      }
    }
  }
}
```
技术上来说，这些是空节点，他们告诉dgraph去创建一个节点，给它一个内部id并且确认它能够被一致地使用。

运行了上面的代码之后，_:company1在dgraph中并不存在，我们也不能去搜索它。我们会发现_:company1已经变成了一个内部id（如上面的运行结果中的uids块）,我们可以搜索这个内部id,使用方法func:uid(<uid_number>)。
让dgraph中的数据产生变化被称作为mutating数据。

+ 怎么样去聚合我们以前的朋友集到现在的公司呢？

不能使用空的节点，因为这些空的节点并不存在，所以我们需要用到uid.
以下为错误示例，因为_:sarah和_:company1都并不存在：

```js
_:sarah <works_for> _:company1 .
```
以下为正确示例：
<uid-for-sarah> <works_for> <uid-for-company1> .

下面这一段用原文吧:
Because the uid picked by Dgraph is unique, we can’t help you this time. Use the uid’s picked by your instance of Dgraph to write a mutation that links the company and friendship data. Hint: previous queries will tell you the uid.
The process you’ve just done here would normally done programmatically - query the data to get the uid’s, formulate the mutations, then batch the updates.


