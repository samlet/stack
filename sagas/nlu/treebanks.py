import io_utils
import os
import json_utils
import json

treebanks_defs="""LANGUAGE	TREEBANK	LANGUAGE CODE	TREEBANK CODE	MODELS	VERSION	TREEBANK LICENSE	TREEBANK DOC	NOTES
Afrikaans	AfriBooms	af	af_afribooms	download	0.2.0	Creative Commons License		 
Ancient Greek	Perseus	grc	grc_perseus	download	0.2.0	Creative Commons License		 
 	PROIEL	grc	grc_proiel	download	0.2.0	Creative Commons License		
Arabic	PADT	ar	ar_padt	download	0.2.0	Creative Commons License		
Armenian	ArmTDP	hy	hy_armtdp	download	0.2.0	Creative Commons License		 
Basque	BDT	eu	eu_bdt	download	0.2.0	Creative Commons License		
Bulgarian	BTB	bg	bg_btb	download	0.2.0	Creative Commons License		
Buryat	BDT	bxr	bxr_bdt	download	0.2.0	Creative Commons License		 
Catalan	AnCora	ca	ca_ancora	download	0.2.0	GNU License		
Chinese (traditional)	GSD	zh	zh_gsd	download	0.2.0	Creative Commons License		
Croatian	SET	hr	hr_set	download	0.2.0	Creative Commons License		
Czech	CAC	cs	cs_cac	download	0.2.0	Creative Commons License		 
 	FicTree	cs	cs_fictree	download	0.2.0	Creative Commons License		 
 	PDT	cs	cs_pdt	download	0.2.0	Creative Commons License		
Danish	DDT	da	da_ddt	download	0.2.0	Creative Commons License		 
Dutch	Alpino	nl	nl_alpino	download	0.2.0	Creative Commons License		
 	LassySmall	nl	nl_lassysmall	download	0.2.0	Creative Commons License		 
English	EWT	en	en_ewt	download	0.2.0	Creative Commons License		
 	GUM	en	en_gum	download	0.2.0	Creative Commons License		 
 	LinES	en	en_lines	download	0.2.0	Creative Commons License		 
Estonian	EDT	et	et_edt	download	0.2.0	Creative Commons License		
Finnish	FTB	fi	fi_ftb	download	0.2.0	GNU License		 
 	TDT	fi	fi_tdt	download	0.2.0	Creative Commons License		 
French	GSD	fr	fr_gsd	download	0.2.0	Creative Commons License		
 	Sequoia	fr	fr_sequoia	download	0.2.0	LGPLLR		 
 	Spoken	fr	fr_spoken	download	0.2.0	Creative Commons License		
Galician	CTG	gl	gl_ctg	download	0.2.0	Creative Commons License		
 	TreeGal	gl	gl_treegal	download	0.2.0	LGPLLR		
German	GSD	de	de_gsd	download	0.2.0	Creative Commons License		
Gothic	PROIEL	got	got_proiel	download	0.2.0	Creative Commons License		
Greek	GDT	el	el_gdt	download	0.2.0	Creative Commons License		
Hebrew	HTB	he	he_htb	download	0.2.0	Creative Commons License		
Hindi	HDTB	hi	hi_hdtb	download	0.2.0	Creative Commons License		
Hungarian	Szeged	hu	hu_szeged	download	0.2.0	Creative Commons License		
Indonesian	GSD	id	id_gsd	download	0.2.0	Creative Commons License		
Irish	IDT	ga	ga_idt	download	0.2.0	Creative Commons License		
Italian	ISDT	it	it_isdt	download	0.2.0	Creative Commons License		 
 	PoSTWITA	it	it_postwita	download	0.2.0	Creative Commons License		 
Japanese	GSD	ja	ja_gsd	download	0.2.0	Creative Commons License		 
Kazakh	KTB	kk	kk_ktb	download	0.2.0	Creative Commons License		 
Korean	GSD	ko	ko_gsd	download	0.2.0	Creative Commons License		 
 	Kaist	ko	ko_kaist	download	0.2.0	Creative Commons License		
Kurmanji	MG	kmr	kmr_mg	download	0.2.0	Creative Commons License		  
Latin	ITTB	la	la_ittb	download	0.2.0	Creative Commons License		
 	Perseus	la	la_perseus	download	0.2.0	Creative Commons License		 
 	PROIEL	la	la_proiel	download	0.2.0	Creative Commons License		 
Latvian	LVTB	lv	lv_lvtb	download	0.2.0	Creative Commons License		
North Sami	Giella	sme	sme_giella	download	0.2.0	Creative Commons License		
Norwegian	Bokmaal	no_bokmaal	no_bokmaal	download	0.2.0	Creative Commons License		
 	Nynorsk	no_nynorsk	no_nynorsk	download	0.2.0	Creative Commons License		
 	NynorskLIA	no_nynorsk	no_nynorsklia	download	0.2.0	Creative Commons License		 
Old Church Slavonic	PROIEL	cu	cu_proiel	download	0.2.0	Creative Commons License		
Old French	SRCMF	fro	fro_srcmf	download	0.2.0	Creative Commons License		
Persian	Seraji	fa	fa_seraji	download	0.2.0	Creative Commons License		
Polish	LFG	pl	pl_lfg	download	0.2.0	GNU License		
 	SZ	pl	pl_sz	download	0.2.0	GNU License		 
Portuguese	Bosque	pt	pt_bosque	download	0.2.0	Creative Commons License		
Romanian	RRT	ro	ro_rrt	download	0.2.0	Creative Commons License		
Russian	SynTagRus	ru	ru_syntagrus	download	0.2.0	Creative Commons License		
 	Taiga	ru	ru_taiga	download	0.2.0	Creative Commons License		
Serbian	SET	sr	sr_set	download	0.2.0	Creative Commons License		
Slovak	SNK	sk	sk_snk	download	0.2.0	Creative Commons License		
Slovenian	SSJ	sl	sl_ssj	download	0.2.0	Creative Commons License		
 	SST	sl	sl_sst	download	0.2.0	Creative Commons License		 
Spanish	AnCora	es	es_ancora	download	0.2.0	GNU License		
Swedish	LinES	sv	sv_lines	download	0.2.0	Creative Commons License		 
 	Talbanken	sv	sv_talbanken	download	0.2.0	Creative Commons License		
Turkish	IMST	tr	tr_imst	download	0.2.0	Creative Commons License		
Ukrainian	IU	uk	uk_iu	download	0.2.0	Creative Commons License		
Upper Sorbian	UFAL	hsb	hsb_ufal	download	0.2.0	Creative Commons License		  
Urdu	UDTB	ur	ur_udtb	download	0.2.0	Creative Commons License		
Uyghur	UDT	ug	ug_udt	download	0.2.0	Creative Commons License		
Vietnamese	VTB	vi	vi_vtb	download	0.2.0	Creative Commons License		
""".split('\n')

class TreeBanks(object):
    def __init__(self):
        self.conf=json_utils.read_json_file('./conf/treebanks.json')

    def query(self, lang_code):
        """
        $ python -m sagas.nlu.treebanks query 'ar'
        :param lang_code:
        :return:
        """
        item = next((x for x in self.conf if x['name'] == lang_code), None)
        return item

    def get_bank_meta(self, treebank, rs):
        target_row = None
        cur_lang = None
        for row in rs:
            if 'LANGUAGE' in row and row['LANGUAGE'].strip() != '':
                cur_lang = row['LANGUAGE']
            if row['TREEBANK CODE'] == treebank:
                target_row = row
                break
        return cur_lang, target_row

    def generate(self):
        """
        $ python -m sagas.nlu.treebanks generate
        :return:
        """
        import sagas

        # prepare the languages table
        langs = []
        lang_tab = []
        for bank in treebanks_defs[1:]:
            parts = bank.split('\t')
            if parts[0].strip() != '':
                langs.append(parts[0])
            lang_tab.append(parts)

        cols = treebanks_defs[0].split('\t')
        df = sagas.to_df(lang_tab, cols)
        rs = json.loads(df.to_json(orient='records'))

        # find all models
        folders = io_utils.list_subdirectories('/pi/ai/corenlp/')
        model_dirs = []
        suffix = '_models'
        for folder in folders:
            if folder.endswith(suffix):
                model_dirs.append((folder))

        # print(model_dirs)
        suffix_len = len(suffix)
        all_models = []
        for dir in model_dirs:
            model_name = os.path.basename(dir)[:-suffix_len]
            lang, meta = self.get_bank_meta(model_name, rs)
            model_idx = {'name': meta['LANGUAGE CODE'], 'lang': lang,
                         'model': model_name, 'version': meta['VERSION'], 'treebank': meta['TREEBANK']}
            all_models.append(model_idx)

        target_file='./conf/treebanks.json'
        json_utils.write_json_to_file(target_file, all_models)
        print('write to', target_file)

treebanks=TreeBanks()

if __name__ == '__main__':
    import fire
    fire.Fire(TreeBanks)