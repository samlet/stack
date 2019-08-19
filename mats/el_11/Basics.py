from sagas.nlu.mats import Cats, Mats

default = Cats('default')

Mats(cat=default) \
    .sent(el="Εμείς διαβάζουμε μία εφημερίδα.",
          en="We read a newspaper.",
          zh="我们读了一份报纸。",
          ja="新聞を読みます。",
          v0="Shinbun o yomimasu.",
          v1="Emeís diavázoume mía efimerída.",
          ) \



