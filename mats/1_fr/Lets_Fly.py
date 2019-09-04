from sagas.nlu.mats import Cats, Mats

default = Cats('default')

Mats(cat=default) \
    .sent(fr="La visite de ce musée était très intéressante grâce au guide.",
          en="The visit of this museum was very interesting thanks to the guide.",
          zh="由于导游，这个博物馆的参观非常有趣。",
          ja="この博物館の訪問は、ガイドのおかげで非常に興味深いものでした。",
          v0="Kono hakubutsukan no hōmon wa, gaido no okage de hijō ni kyōmibukai monodeshita.",
          ) \
    .sent(fr="Je vous souhaite un agréable séjour.",
          en="I wish you a pleasant stay.",
          zh="祝你愉快。",
          ja="快適なご滞在をお祈りしています。",
          v0="Kaitekina go taizai o oinori shite imasu.",
          ) \
    .sent(fr="Il pleure parce que le concert était complet",
          en="He's crying because the concert was complete",
          zh="他哭了，因为演唱会很完整",
          ja="コンサートが終わったので彼は泣いています",
          v0="Konsāto ga owattanode kare wa naite imasu",
          ) \
    .sent(en="He's crying because the concert was complete",
          zh="他哭是因为音乐会结束了",
          ja="コンサートが完成したので彼は泣いている",
          ) \
    .sent(fr="Je bois un café, sinon je vais dormir.",
          en="I drink a coffee, otherwise I go to sleep.",
          zh="我喝咖啡，否则我会去睡觉。",
          ja="私はコーヒーを飲み、そうでなければ私は眠りにつく。",
          v0="Watashi wa kōhī o nomi,-sōdenakereba watashi wa nemurinitsuku.",
          ) \

