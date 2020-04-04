# procs-cli-routines.md
## prepare
```sh
$ python -m sagas.nlu.treebanks generate
```

## start
```sh
$ sel 'Ο διαιτητής είναι από το Βέλγιο.'
$ sko '언어를 배우는 것은 흥미로워요.'
$ sko '우리는 사람들과 말하고 싶어요.'
$ si 'Gli piace ascoltare la musica.'

$ sj 'ブラジルは 南米に あります 。'
$ sj 'なぜ あなたは 時間どおりに 来られなかったの です か ？'

$ snl 'Maar het boek was beter dan de film.'
$ se 'The film was not boring.'
$ se 'The similarity between these two sentences'
$ sz '你 学习 西班牙语 。'
$ st 'İnsanlar ile konuşmak istiyoruz.'
$ saf 'Waarheen gaan hulle graag?'

$ nlu clip_parse fi 'Tuolla ylhäällä asuu vanha nainen.'
$ nlu clip_parse et 'Tema on siin ja tema on siin.'

$ nluc hi 'मेरा परिवार यहाँ'
$ nluc lt 'Ji dirba prie kompiuterio.'
```

+ datetime

```sh
$ sd 'Die Aufnahmen begannen im November.'
$ domains 'Die Aufnahmen begannen im November.' de
```

+ wordnet

```sh
$ def 主持人 zh
```




