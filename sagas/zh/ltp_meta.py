import sagas

# https://ltp.readthedocs.io/zh_CN/latest/appendix.html#id6
# https://www.ltp-cloud.com/intro#srl_how
'''
核心的语义角色为 A0-5 六种，A0 通常表示动作的施事，A1通常表示动作的影响等，A2-5 根据谓语动词不同会有不同的语义含义。
其余的15个语义角色为附加语义角色，如LOC 表示地点，TMP 表示时间等。
'''
descs='''标记	说明
ADV	adverbial, default tag ( 附加的，默认标记 )
BNE	beneﬁciary ( 受益人 )
CND	condition ( 条件 )
DIR	direction ( 方向 )
DGR	degree ( 程度 )
EXT	extent ( 扩展 )
FRQ	frequency ( 频率 )
LOC	locative ( 地点 )
MNR	manner ( 方式 )
PRP	purpose or reason ( 目的或原因 )
TMP	temporal ( 时间 )
TPC	topic ( 主题 )
CRD	coordinated arguments ( 并列参数 )
PRD	predicate ( 谓语动词 )
PSR	possessor ( 持有者 )
PSE	possessee ( 被持有 )'''

def get_role_defs():
    desc_rs = []
    for desc in descs.split('\n')[1:]:
        desc_rs.append(desc.split('\t'))
    return sagas.to_df(desc_rs, ['mark', 'description'])

dep_defs='''主谓关系	SBV	subject-verb	我送她一束花 (我 <– 送)
动宾关系	VOB	直接宾语，verb-object	我送她一束花 (送 –> 花)
间宾关系	IOB	间接宾语，indirect-object	我送她一束花 (送 –> 她)
前置宾语	FOB	前置宾语，fronting-object	他什么书都读 (书 <– 读)
兼语	DBL	double	他请我吃饭 (请 –> 我)
定中关系	ATT	attribute	红苹果 (红 <– 苹果)
状中结构	ADV	adverbial	非常美丽 (非常 <– 美丽)
动补结构	CMP	complement	做完了作业 (做 –> 完)
并列关系	COO	coordinate	大山和大海 (大山 –> 大海)
介宾关系	POB	preposition-object	在贸易区内 (在 –> 内)
左附加关系	LAD	left adjunct	大山和大海 (和 <– 大海)
右附加关系	RAD	right adjunct	孩子们 (孩子 –> 们)
独立结构	IS	independent structure	两个单句在结构上彼此独立
核心关系	HED	head	指整个句子的核心'''.split('\n')

def get_dep_defs():
    def_rs=[]
    for dep in dep_defs:
        def_rs.append(dep.split('\t'))
    return sagas.to_df(def_rs, ['type', 'tag', 'desc', 'example'])

# https://ltp.readthedocs.io/zh_CN/latest/appendix.html#id3
# LTP 使用的是863词性标注集，其各个词性含义如下表
pos_defs='''a	adjective	美丽	ni	organization name	保险公司
b	other noun-modifier	大型, 西式	nl	location noun	城郊
c	conjunction	和, 虽然	ns	geographical name	北京
d	adverb	很	nt	temporal noun	近日, 明代
e	exclamation	哎	nz	other proper noun	诺贝尔奖
g	morpheme	茨, 甥	o	onomatopoeia	哗啦
h	prefix	阿, 伪	p	preposition	在, 把
i	idiom	百花齐放	q	quantity	个
j	abbreviation	公检法	r	pronoun	我们
k	suffix	界, 率	u	auxiliary	的, 地
m	number	一, 第一	v	verb	跑, 学习
n	general noun	苹果	wp	punctuation	，。！
nd	direction noun	右侧	ws	foreign words	CPU
nh	person name	杜甫, 汤姆	x	non-lexeme	萄, 翱
 	 	 	z	descriptive words	瑟瑟，匆匆'''.split('\n')

def get_pos_defs():
    pos_rs=[]
    for pos in pos_defs:
        parts=pos.split('\t')
        pos_rs.append(parts[:3])
        pos_rs.append(parts[3:])
    return sagas.to_df(pos_rs, ['tag','desc','example'])

class LtpMeta(object):
    def __init__(self):
        self.roles_df=get_role_defs()
        self.dep_defs=get_dep_defs()
        self.pos_defs=get_pos_defs()

    def defs(self):
        """
        $ python -m sagas.zh.ltp_meta defs
        :return:
        """
        sagas.print_df(self.roles_df)
        sagas.print_df(self.dep_defs)
        sagas.print_df(self.pos_defs)

if __name__ == '__main__':
    import fire
    fire.Fire(LtpMeta)