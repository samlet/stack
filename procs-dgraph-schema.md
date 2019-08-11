# procs-dgraph-schema.md
## 一些重点
⊕ [Dgraph-Take a tour - 简书](https://www.jianshu.com/p/63760573d2cf)

* fulltext和term: 全文搜索是Google用于网页的。这种查询很难用term匹配，因为这种查询试图遵从语言、语法以及时态. 例如, “run”的全文搜索匹配项包含“run”、“running”、“ran”, 全文搜索不会准确地匹配项, 而是利用：
  词干：找到不同时态、单复数等词的公共部分，
  停止词：移除and、or、it等过于常见的词

```js
{
  movie(func:alloftext(name@en, "the man runs"))
    @filter(has(genre))
  {
    name@en
  }
}
```

## scalar
default 串
int Int64的
float   浮动
string  串
bool    布尔
dateTime    time.Time（RFC3339格式[可选时区]例如：2006-01-02T15：04：05.999999999 + 10:00或2006-01-02T15：04：05.999999999）
geo 去-GEOM
password    字符串（加密）

uid UINT64

## schema
```js
name: string @index(exact, fulltext) @count .
multiname: string @lang .
age: int @index(int) .
friend: uid @count .
dob: dateTime .
location: geo @index(geo) .
occupations: [string] @index(term) .
```
```js
name: string @index(exact) .
friend: uid @reverse .
age: int .
married: bool .
loc: geo .
dob: datetime .
```
* @index使用参数指定索引，指定tokenizer。为谓词指定索引时，必须指定索引的类型。
* term 允许在句子中按术语搜索。
* trigram 正则表达式匹配。也可以用于等式检查。
* exact 允许更快的排序。
* hash，exact，term，或者fulltext  性能最高的指标eq是hash。仅使用term或者fulltext您还需要术语或全文搜索。如果您已经在使用term，则无需使用hash或使用exact。

```js
  name: string @index(term) .
  url: string .
  description: string @index(fulltext) .
```
```js
{
  set {
    _:dgraph <name> "Dgraph" .
    _:dgraph <url> "https://github.com/dgraph-io/dgraph" .
    _:dgraph <description> "Fast, Transactional, Distributed Graph Database." .
  }
}
```
```sh
curl localhost:8080/alter -XPOST -d $'
  name: string @index(term) .
  release_date: datetime @index(year) .
  revenue: float .
  running_time: int .
' | python -m json.tool | less
```

## i18n
```js
<职业>: string @index(exact) .
<年龄>: int @index(int) .
<地点>: geo @index(geo) .
<公司>: string .
```
支持谓词名称和值的国际化资源标识符（IRI）。
如果您的谓词是URI或具有特定于语言的字符，则<>在执行模式变异时用尖括号将其括起来。
此语法允许国际化谓词名称，但全文索引仍默认为英语。要为您的语言使用正确的标记化程序，您需要使用该@lang指令并使用您的语言标记输入值。

```js
<公司>: string @index(fulltext) @lang .
```

+ 突变：

```js
{
  set {
    _:a <公司> "Dgraph Labs Inc"@en .
    _:b <公司> "夏新科技有限责任公司"@zh .
  }
}
```

+ 查询：

```js
{
  q(func: alloftext(<公司>@zh, "夏新科技有限责任公司")) {
    _predicate_
  }
}
```

## Upsert指令
@upsert如果要对其进行upsert操作，谓词可以在模式中指定该指令。如果@upsert指定了该指令，则在提交事务时将检查谓词的索引键是否存在冲突。该@upsert指令有助于在运行并发upsert时强制执行唯一性约束。
这是为谓词指定upsert指令的方法。

```js
email: string @index(exact) @upsert .
```

## 索引
注意通过应用函数对谓词进行过滤需要索引。
可以索引所有标量类型。

+ 可用于字符串的索引如下。

Dgraph功能    必需的索引/标记生成器 笔记
eq  hash，exact，term，或者fulltext  性能最高的指标eq是hash。仅使用term或者fulltext您还需要术语或全文搜索。如果您已经在使用term，则无需使用hash或使用exact。
le，ge，lt，gt exact   允许更快的排序。
allofterms，anyofterms   term    允许在句子中按术语搜索。
alloftext，anyoftext fulltext    与语言特定的词干和停用词匹配。
regexp  trigram 正则表达式匹配。也可以用于等式检查。

+ 可用的指数dateTime如下。

索引名称/ Tokenizer 部分日期已编入索引
year    年度指数（默认）
month   年和月的指数
day 年，月，日指数
hour    年，月，日和小时的指数
dateTime索引的选择允许选择索引的精度。应用程序，例如这些文档中的电影示例，需要搜索日期但每年节点相对较少，可能更喜欢year标记器; 依赖于细粒度日期搜索的应用程序（例如实时传感器读数）可能更喜欢hour索引。
所有dateTime指数都是可排序的。

+ 计数指数

对于@count Dgraph索引的谓词，每个节点的边数。这样可以快速查询表单：

```js
{
  q(func: gt(count(pred), threshold)) {
    ...
  }
}
```

+ list

如果在模式中指定，带标量类型的谓词也可以存储值列表。标量类型需要包含在其中[]以指示其列表类型。这些列表就像一个无序集。

```js
occupations: [string] .
score: [int] .
```
•   设置操作会添加到值列表中。存储值的顺序是不确定的。
•   删除操作将从列表中删除该值。
•   查询这些谓词将返回数组中的列表。
•   索引可以应用于具有列表类型的谓词，您可以对它们使用函数。
•   使用这些谓词不允许排序。

```js
testList: [string] .
```
```json
{
  "testList": [
    "Grape",
    "Apple",
    "Strawberry",
    "Banana",
    "watermelon"
  ]
}
```
从这个列表中删除或添加“Apple”:

```js
{
   "uid": "0xd", #UID of the list.
   "testList": "Apple"
}
```

## 反向边缘
图形边缘是单向的。对于节点 - 节点边缘，有时建模需要反向边缘。如果只有一些主题 - 谓词 - 对象三元组具有反转，则必须手动添加这些三元组。但是如果谓词总是反转，则Dgraph计算反向边缘，如果@reverse在模式中指定的话。
反面anEdge是~anEdge。

## 查询架构
架构查询查询整个架构：
schema {}


