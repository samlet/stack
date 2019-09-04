from sagas.nlu.mats import Cats, Mats

default = Cats('default')

Mats(cat=default) \
    .sent(ar="كَلْبَك جَوْعان يا جورْج.",
          en="Your dog is hungry, George.",
          zh="你的狗饿了，乔治。",
          ja="ジョージ、おなかがすいています。",
          v0="Jōji, onaka ga suite imasu.",
          v1="kalbak jawean ya jwrj.",
          ) \
    .sent(ar="هُوَّ كَلْبِك يا مَها.",
          en="He is your dog, Maha.",
          zh="他是你的狗，玛哈。",
          ja="彼はあなたの犬、マハです。",
          v0="Kare wa anata no inu, Mahadesu.",
          v1="huww kalbik ya maha.",
          ) \
    .sent(ar="زَوْجِك مُمْتاز يا ريم.",
          en="Your husband is excellent, Rim.",
          zh="你丈夫很优秀，Rim。",
          ja="あなたの夫は素晴らしいです、リム。",
          v0="Anata no otto wa subarashīdesu, rimu.",
          v1="zawjik mumtaz ya rim.",
          ) \
    .sent(ar="هُوَّ ابْنِك وَهُوَّ سَعيد يا سامْية.",
          en="He is your son and he is happy, Samia.",
          zh="他是你的儿子，他很高兴，萨米亚。",
          ja="彼はあなたの息子であり、彼は幸せです、サミア。",
          v0="Kare wa anata no musukodeari, kare wa shiawasedesu, samia.",
          v1="huww abnik wahuww saeyd ya samy.",
          ) \
    .sent(ar="هِيَّ بِنْتَك يا بوب.",
          en="She is your daughter, Bob.",
          zh="她是你的女儿鲍勃。",
          ja="彼女はあなたの娘、ボブです。",
          v0="Kanojo wa anata no musume, Bobudesu.",
          v1="hi bintak ya bub.",
          ) \
    .sent(ar="كَراجَك بارِد يا سام.",
          en="Your garage is cold, Sam.",
          zh="山姆，你的车库很冷。",
          ja="ガレージは寒いです、サム。",
          v0="Garēji wa samuidesu, Samu.",
          v1="karajak barid ya sam.",
          ) \
    .sent(ar="كَراجِك مُمْتاز يا سامْية.",
          en="Your garage is excellent, Samia.",
          zh="萨米亚，你的车库很棒。",
          ja="あなたのガレージは素晴らしいです、サミア。",
          v0="Anata no garēji wa subarashīdesu, samia.",
          v1="karajik mumtaz ya samy.",
          ) \
    .sent(ar="أَيْن بَيْتَك يا سام؟",
          en="Where is your house, Sam?",
          zh="山姆，你的房子在哪里？",
          ja="あなたの家はどこですか、サム？",
          v0="Anata no ie wa dokodesu ka, Samu?",
          v1="'ayn baytak ya sam?",
          ) \
    .sent(ar="جاكيتَك جَديد يا سام.",
          en="Your jacket is new, Sam.",
          zh="你的夹克是新的，Sam。",
          ja="あなたのジャケットは新しいです、サム。",
          v0="Anata no jaketto wa atarashīdesu, Samu.",
          v1="jakytak jadyd ya sam.",
          ) \
    .sent(ar="بَيْتي بَيْتِك يا سامْية.",
          en="My house, your house, Samia.",
          zh="我的房子，你的房子，萨米亚。",
          ja="私の家、あなたの家、サミア。",
          v0="Watashinoie, anata no ie, samia.",
          v1="bayty baytik ya samy.",
          ) \
    .sent(ar="جارَك عُمَر مُتَرْجِم سَريع يا مايْك.",
          en="Your neighbor Omar is a fast translator, Mike.",
          zh="你的邻居奥马尔是一名快速翻译，迈克。",
          ja="隣人のオマールは速い翻訳者、マイクです。",
          v0="Rinjin no omāru wa hayai hon'yaku-sha, maikudesu.",
          v1="jarak eumar mutarjim sarye ya mayk.",
          ) \
    .sent(ar="جارَك عُمَر مُتَرْجِم يا رَواد.",
          en="Your neighbor Omar is an interpreter, pioneers.",
          zh="你的邻居奥马尔是一名翻译，开拓者。",
          ja="隣人のオマールは通訳者であり、先駆者です。",
          v0="Rinjin no omāru wa tsūyaku-shadeari, senku-shadesu.",
          v1="jarak eumar mutarjim ya rawad.",
          ) \



