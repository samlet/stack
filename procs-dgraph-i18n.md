# procs-dgraph-i18n.md
⊕ [How should the @lang field be saved using JSON (with the Go package)? - Users / Dgraph - Discuss Dgraph](https://discuss.dgraph.io/t/how-should-the-lang-field-be-saved-using-json-with-the-go-package/3026/2)

Using mutation in JSON you can simply use <"predicate + @ + Lang">

e.g in JSON format:

```json
{
    "set": [
        {
            "name@en": "english",
            "name@ru": "Russian",
            "TEST": "X"
        },
        {
            "name": "Amit",
            "name@ru": "Russian"
        }
    ]
}
```

⊕ [Query language — Dgraph Doc v1.0.14](https://docs.dgraph.io/query-language/#full-text-search)

Following table contains all supported languages, corresponding country-codes, stemming and stop words filtering support.

Language    Country Code    Stemming    Stop words
---------------------------------------------------
Arabic  ar  ✓   ✓
Armenian    hy      ✓
Basque  eu      ✓
Bulgarian   bg      ✓
Catalan ca      ✓
Chinese zh  ✓   ✓
Czech   cs      ✓
Danish  da  ✓   ✓
Dutch   nl  ✓   ✓
English en  ✓   ✓
Finnish fi  ✓   ✓
French  fr  ✓   ✓
Gaelic  ga      ✓
Galician    gl      ✓
German  de  ✓   ✓
Greek   el      ✓
Hindi   hi  ✓   ✓
Hungarian   hu  ✓   ✓
Indonesian  id      ✓
Italian it  ✓   ✓
Japanese    ja  ✓   ✓
Korean  ko  ✓   ✓
Norwegian   no  ✓   ✓
Persian fa      ✓
Portuguese  pt  ✓   ✓
Romanian    ro  ✓   ✓
Russian ru  ✓   ✓
Spanish es  ✓   ✓
Swedish sv  ✓   ✓
Turkish tr  ✓   ✓

