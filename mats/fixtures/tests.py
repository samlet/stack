from sagas.nlu.mats import Cats, Mats

default = Cats('default')

Mats(cat=default) \
    .sent(fr="L'auberge de jeunesse n'est pas chère.",
          en="The hostel is not expensive.",
          zh="宿舍不贵。",
          ja="ホステルは高価ではありません。",
          v1="Hosuteru wa kōkade wa arimasen.",
          ) \
    .sent(fr="L'auberge de jeunesse n'est pas chère.",
          en="The hostel is not expensive.",
          zh="宿舍不贵。",
          ja="ホステルは高価ではありません。",
          v1="Konsāto ga owattanode kare wa naite imasu",
          ) \

fr_house = Cats('house')
Mats(cat=fr_house) \
    .sent(fr="L'auberge de jeunesse n'est pas chère.",
          en="The hostel is not expensive.",
          zh="宿舍不贵。",
          ja="ホステルは高価ではありません。",
          v1="Hosuteru wa kōkade wa arimasen.",
          ) \
    .sent(fr="L'auberge de jeunesse n'est pas chère.",
          en="The hostel is not expensive.",
          zh="宿舍不贵。",
          ja="ホステルは高価ではありません。",
          v1="Konsāto ga owattanode kare wa naite imasu",
          ) \
    .sent(fr="L'auberge de jeunesse n'est pas chère.",
          en="The hostel is not expensive.",
          zh="宿舍不贵。",
          ja="ホステルは高価ではありません。",
          v0="Hosuteru wa kōkade wa arimasen.",
          ) \
    .sent(fr="Nous n'avons rencontré personne.",
          en="We did not meet anyone.",
          zh="我们没有见过任何人。",
          ja="私たちは誰にも会いませんでした。",
          v0="Watashitachiha darenimo aimasendeshita.",
          ) \
    .sent(fr="Je vous souhaite un agréable séjour.",
          en="I wish you a pleasant stay.",
          zh="祝你愉快。",
          ja="快適なご滞在をお祈りしています。",
          v0="Kaitekina go taizai o oinori shite imasu.",
          ) \
    .sent(fr="La visite de ce musée était très intéressante grâce au guide.",
          en="The visit of this museum was very interesting thanks to the guide.",
          zh="由于导游，这个博物馆的参观非常有趣。",
          ja="この博物館の訪問は、ガイドのおかげで非常に興味深いものでした。",
          v0="Kono hakubutsukan no hōmon wa, gaido no okage de hijō ni kyōmibukai monodeshita.",
          ) \



