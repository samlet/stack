# procs-graphviz.md
⊕ [User Guide — graphviz 0.10.1 documentation](https://graphviz.readthedocs.io/en/stable/manual.html)
⊕ [graphviz/manual.rst at 1377ec44eb7431c728a21f5739297c087385b3b4 · xflr6/graphviz](https://github.com/xflr6/graphviz/blob/1377ec44eb7431c728a21f5739297c087385b3b4/docs/manual.rst)

⊕ [Examples — graphviz 0.10.1 documentation](https://graphviz.readthedocs.io/en/stable/examples.html)
⊕ [Node, Edge and Graph Attributes](https://www.graphviz.org/doc/info/attrs.html)
⊕ [Forever For Now - UML Diagrams Using Graphviz Dot](http://www.ffnn.nl/pages/articles/media/uml-diagrams-using-graphviz-dot.php)

+ procs-graphviz.ipynb
+ procs-ofbiz-model-graph.ipynb

⊕ [Node, Edge and Graph Attributes](https://www.graphviz.org/doc/info/attrs.html#k:style)
    Basic style settings for nodes; 
    Basic style settings for edges; 
    ⊕ [Color Names](https://www.graphviz.org/doc/info/colors.html)

## 解决显示Arabic文本的问题
⊕ [GraphVizio – A Graphviz addin for Visio » Maurice's Musings](https://www.calvert.ch/maurice/2010/05/11/graphvizio-a-graphviz-addin-for-visio/)
    * 改变字体: fontname=Calibri

```dot
graph  RootGraph {
  node [width="7.08661417322834", height="0.787401574803148", color="#000000", fillcolor="#FFFFFF", fontname=Calibri, fontsize=24, style=filled, shape=box];
  edge [color="#000000", fillcolor="#FFFFFF"];

  "English: Hello, my name is Maurice\n(and blame Google if the translations are bad)" [pos="283.704566929134,620.932913385827", label="English: Hello, my name is Maurice\n(and blame Google if the translations are bad)"];
  "Russian: Здравствуйте, меня зовут Морис" [pos="283.704566929134,526.932913385827", label="Russian: Здравствуйте, меня зовут Морис"];
  "مرحبا، اسمي موريس : Arabic" [pos="283.704566929134,432.932913385827", label="مرحبا، اسمي موريس : Arabic"];
  "Chinese: 你好，我叫莫里斯" [pos="283.704566929134,338.932913385827", label="Chinese: 你好，我叫莫里斯"];
  "שלום, שמי הוא מוריס : Hebrew" [pos="283.704566929134,244.932913385827", label="שלום, שמי הוא מוריס : Hebrew"];
  "Japanese: こんにちは、私の名前はモーリスです" [pos="283.704566929134,150.932913385826", label="Japanese: こんにちは、私の名前はモーリスです"];
  "Thai: สวัสดีชื่อของฉันคือ Maurice" [pos="283.704566929134,56.9329133858268", label="Thai: สวัสดีชื่อของฉันคือ Maurice"];

  "English: Hello, my name is Maurice\n(and blame Google if the translations are bad)"--"Russian: Здравствуйте, меня зовут Морис";
  "Russian: Здравствуйте, меня зовут Морис"--"مرحبا، اسمي موريس : Arabic";
  "مرحبا، اسمي موريس : Arabic"--"Chinese: 你好，我叫莫里斯";
  "Chinese: 你好，我叫莫里斯"--"שלום, שמי הוא מוריס : Hebrew";
  "שלום, שמי הוא מוריס : Hebrew"--"Japanese: こんにちは、私の名前はモーリスです";
  "Japanese: こんにちは、私の名前はモーリスです"--"Thai: สวัสดีชื่อของฉันคือ Maurice";
}
```

