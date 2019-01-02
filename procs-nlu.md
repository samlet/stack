# procs-nlu.md
## start
```sh
$ cd examples/formbot/
$ make train-nlu

$ open http://localhost:8890/notebooks/procs-nlu.ipynb
```

## featurizer
⊕ [我们使用Rasa构建聊天机器人的经验 - 调整NLU管道](https://chatbotslife.com/our-experience-building-chatbots-with-rasa-tuning-the-nlu-pipeline-74a80cd565b8)

我们主要用于intent_featurizer_count_vectors从令牌中提取特征，因为它是Tensorflow分类器的推荐特征。我们调整了几个参数以获得更好的结果。

首先，有一个正则表达式定义哪些令牌将被视为特征，默认正则表达式排除只有一个字符的单词。这对于英语来说可能没问题，但在韩语中，单个字符집就是一个你不想丢失的实际单词。即使是英语，how r u?如果您考虑r并u作为功​​能，也可能只能被正确识别。

默认正则表达式是(?u)\b\w\w+\b，您可以将其更改(?u)\b\w+\b为包含单字符单词。

另一个有趣的调整是增加n-gram的数量，默认为1。通过使用max_ngram2，您将为每对连续的单词创建其他功能。例如，如果您想要识别I'm happy和I'm not happy作为不同的意图，它有助于not happy作为一个功能。

```
-  name：“intent_featurizer_count_vectors”
   token_pattern：'（？u）\ b \ w + \ 
  b'max_ngram：2
```

最后要注意的是，如果在训练数据中包含正则表达式模式，则必须intent_entity_featurizer_regex在管道中包含该组件，否则将忽略它们。

## ner
使用预先训练好的命名实体识别器，ner_spacy或者ner_duckling非常简单，配置不多。另一方面，您可以使用ner_crf组件定义自己的实体。

如果您在管道中使用spaCy，请确保您的ner_crf组件实际上通过向列表添加pos和pos2功能来使用词性标记。这两个功能默认包含在版本0.12.3之前，但是下一个版本可以在ner_crf没有spaCy的情况下使用，因此默认值被更改为NOT包含它们。

在我们的测试中，词性标注产生了巨大的差异。例如，在机器人询问“你的名字是什么？”之后，我们有意让用户提供他们的名字。

```
## intent：give_name
 -  [John]（姓名）
......
```

如果没有词性特征，命名实体识别器就无法区分新名称（不在训练示例中）和像“Hi”这样的输入：它开始识别任何以单词开头的单词大写字母作为我们的name实体。一旦我们添加了这些pos功能，就不会再出现混乱。

要准确了解每个功能的作用，您可以直接参考代码。选择哪些功能实际上取决于域和语言（例如韩语，upper并且title没用，因为没有外壳）。下面的列表显示了添加了词性功能的新默认值。

```
-  name：ner_crf
   features：[ 
    [“low”，“title”，“upper”]，
    [“bias”，“low”，“prefix5”，“prefix2”，“suffix5”，“suffix3”，“suffix2”， “upper”，“title”，“digit”，“pattern”，“pos”，“pos2”]，
    [“low”，“title”，“upper”]]
```    
与此类似intent_entity_featurizer_regex，如果您在训练数据中定义了同义词，请不要忘记添加ner_synonyms到管道中。这很容易忘记！


