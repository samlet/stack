from sagas.nlu.mats import Cats, Mats

default = Cats('default')

Mats(cat=default) \
    .sent(en="we are a family",
          fr="nous sommes une famille",
          zh="我们是一家人",
          ko="우리는 가족이다",
          v0="ulineun gajog-ida",
          ) \
    .sent(en="what is your name",
          fr="quel est votre nom",
          zh="你叫什么名字",
          ko="당신의 이름은 무엇입니까",
          v0="dangsin-ui ileum-eun mueos-ibnikka",
          t0="dang-sin-eui i-reum-eun mu-eos-ib-ni-gga",
          ) \
    .sent(en="i am pleased to meet you",
          fr="Je suis heureux de vous rencontrer",
          zh="我很高兴见到你",
          ko="만나서 반가워",
          v0="mannaseo bangawo",
          t0="man-na-seo ban-ga-weo",
          ) \
    .sent(en="do you like it here",
          fr="est-ce que tu l'aimes ici",
          zh="你喜欢这里吗",
          ko="이곳을 좋아하세요",
          v0="igos-eul joh-ahaseyo",
          t0="i-gos-eur joh-a-ha-se-yo",
          ) \
    .sent(en="the family is not small",
          fr="la famille n'est pas petite",
          zh="这个家庭不小",
          ko="가족은 작지 않다",
          v0="gajog-eun jagji anhda",
          t0="ga-jog-eun jag-ji anh-da",
          ) \
    .sent(en="the family is big",
          fr="la famille est grande",
          zh="这个家庭很大",
          ko="가족은 크다",
          v0="gajog-eun keuda",
          t0="ga-jog-eun keu-da",
          ) \
    .sent(en="i learn english",
          fr="j'apprends l'anglais",
          zh="我学习英语",
          ko="나는 영어를 배운다",
          v0="naneun yeong-eoleul baeunda",
          t0="na-neun yeong-eo-reur bae-un-da",
          ) \
    .sent(en="you learn",
          fr="vous apprenez",
          zh="你学",
          ko="너는 배우다",
          v0="neoneun baeuda",
          t0="neo-neun bae-u-da",
          ) \
    .sent(en="he learns",
          fr="il apprend",
          zh="他学习",
          ko="그는 배운다",
          v0="geuneun baeunda",
          t0="geu-neun bae-un-da",
          ) \
    .sent(en="i learn english",
          fr="j'apprends l'anglais",
          zh="我学习英语",
          ko="나는 영어를 배운다",
          v0="naneun yeong-eoleul baeunda",
          t0="na-neun yeong-eo-reur bae-un-da",
          ) \
    .sent(en="this is the teacher",
          fr="c'est l'enseignant",
          zh="这是老师",
          ko="이것은 선생님입니다",
          v0="igeos-eun seonsaengnim-ibnida",
          t0="i-geos-eun seon-saeng-nim-ib-ni-da",
          ) \
    .sent(en="we are learning",
          fr="nous apprenons",
          zh="我们正在学习",
          ko="우린 배우는 중이다",
          v0="ulin baeuneun jung-ida",
          t0="u-rin bae-u-neun jung-i-da",
          ) \
    .sent(en="we learn french",
          fr="nous apprenons le français",
          zh="我们学法语",
          ko="우리는 프랑스어를 배웁니다",
          v0="ulineun peulangseueoleul baeubnida",
          t0="u-ri-neun peu-rang-seu-eo-reur bae-ub-ni-da",
          ) \







