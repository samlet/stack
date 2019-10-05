text_raw='''最近的 邮局 在哪？
‫نزدیکترین ‫پستخانه کجاست؟‬
postkhâne-ye ba-adi kojâst?
►
到 最近的 邮局 远 吗 ？
‫تا نزدیکترین پستخانه خیلی راه است؟‬
tâ postkhâne-ye ba-adi khyli râh ast?
►
最近的 邮箱 在 哪儿 ？
‫نزدیکترین ‫صندوق پست کجاست؟‬
sandughe poste ba-adi kojâst?
►
我 需要 一些 邮票 。
‫من تعدادی تمبر لازم دارم.‬
man te-edâdi tambr lâzem dâram.
►
为了 一个 明信片 和 一封 信 。
‫برای یک کارت پستال و یک نامه.‬
barâye yek kârt postâl va yek nâmeh.
►
邮到 美国/美洲 要 多少钱 ？
‫هزینه ارسال به آمریکا چقدراست؟‬
hazine-ye ersâl be âmrikâ cheghadr ast?
►
这个 邮包 多重 ？
‫وزن بسته چقدر است؟‬
vazne baste cheghadr ast?
►
我 能 航空邮件 邮寄 它（包裹） 吗 ？
‫می‌توانم آن را با پست هوایی ارسال کنم؟‬
mitavânam ân râ bâ poste havâ-i ersâl konam?
►
多久 才 能 到 ？
‫چقدر طول می‌کشد تا بسته به مقصد برسد؟‬
che mod-dat tool mikeshad tâ mahmule be maghsad beresad?
►
我 在哪里 能 打电话 ？ 我 能 在哪里 打电话 ？
‫کجا می‌توانم تلفن بزنم؟‬
kojâ mitavânam telefon bezanam?
►
最近的 电话亭 在 哪里 ？
‫نزدیکترین باجه تلفن کجاست؟‬
bâje-ye telefone ba-adi kojâst?
►
您 有 电话卡 吗 ？
‫کارت تلفن دارید؟‬
kârte telefon dârid?
►
你 有 电话号码本 吗 ？
‫دفترچه تلفن دارید؟‬
daftar-che telefon dârid?
►
您 知道 奥地利的 前拨号 吗 ？
‫پیش شماره کشور اتریش را می‌دانید؟‬
pish shomâre-ye keshvare otrish râ midânid?
►
等 一会儿， 我 看一下 。
‫یک لحظه، نگاه می‌کنم.‬
yek lahze, miravam negâh konam.
►
电话 总是 占线 。
‫تلفن همیشه اشغال است.‬
telefon hamishe eshghâl ast.
►
您拨的 哪个 电话号码 ？
‫چه شماره ای را گرفتید؟‬
che shomâre-e râ gereftid?
►
您 必须 首先 拨0 ！
‫اول باید صفر را بگیرید.‬
ebtedâ bâyad adade sefr râ begirid.'''.split('►')

print(len(text_raw))
el=text_raw[0].split('\n')
print(el[0], '..', el[2])
print(el[1])

import sagas
fa=lambda s: sagas.dia('fa', local_translit=True).ana(s)
fa(el[1])

