from sagas.nlu.mats import Cats, Mats

default = Cats('default')

Mats(cat=default) \
    .sent(en="we learn french",
          fr="nous apprenons le français",
          zh="我们学法语",
          hi="हम फ्रेंच सीखते हैं",
          v0="ham phrench seekhate hain",
          t0="hm french sikhte han",
          ) \
    .sent(en="good afternoon",
          fr="bonne après-midi",
          zh="下午好",
          hi="नमस्कार",
          v0="namaskaar",
          t0="nmskar",
          ) \
    .sent(en="good night",
          fr="bonne nuit",
          zh="晚安",
          hi="शुभ रात्रि",
          v0="shubh raatri",
          t0="shubh ratri",
          ) \
    .sent(en="what is your name",
          fr="quel est votre nom",
          zh="你叫什么名字",
          hi="तुम्हारा नाम क्या हे",
          v0="tumhaara naam kya he",
          t0="tuamhara nam kya he",
          ) \
    .sent(en="i have a cat",
          fr="j'ai un chat",
          zh="我有一只猫",
          hi="मेरे पास एक बिल्ली है",
          v0="mere paas ek billee hai",
          t0="mere pas ak billi ha",
          ) \
    .sent(en="i have a car",
          fr="j'ai une voiture",
          zh="我有一辆车",
          hi="मेरे पास एक कार है",
          v0="mere paas ek kaar hai",
          t0="mere pas ak kar ha",
          ) \
    .sent(en="i have a hobby",
          fr="j'ai un passe-temps",
          zh="我有一个爱好",
          hi="मेरा एक शौक है",
          v0="mera ek shauk hai",
          t0="mera ak shauk ha",
          ) \
    .sent(en="i drink coffee",
          fr="je bois du café",
          zh="我喝咖啡",
          hi="मुझे कॉफी पीना है",
          v0="mujhe kophee peena hai",
          t0="mujhe kophi pina hai",
          ) \
    .sent(en="this is my mother",
          fr="c'est ma mère",
          zh="这是我的母亲",
          hi="यह मेरी माँ है",
          v0="yah meree maan hai",
          t0="yaha meri mam hai",
          ) \
    .sent(en="this is my daughter",
          fr="c'est ma fille",
          zh="这是我的女儿",
          hi="यह मेरी बेटी हैं",
          v0="yah meree betee hain",
          t0="yaha meri beti haim",
          ) \






