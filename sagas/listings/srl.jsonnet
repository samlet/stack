{
    BertSrl: {
        'type': 'sagas.listings.srl.bert_srl_co.BertSrlCo',
        'model': ''
    },
    LtpSrl: {
        'type': 'sagas.listings.srl.ltp_srl_co.LtpSrlCo',
        'pipelines': ['pos', 'ner'],
    },
    LtpSrl2: {
        'type': 'sagas.listings.srl.ltp_srl_co.LtpSrlCo',
        'pipelines': ['pos'],
    },

    Examples: {
        // $ list srl basic
        basic: {
            conf: "BertSrl",
            input: { sentence: "Hugging Face is a technology company based in New York and Paris" }
            },
        // $ list srl ltp
        ltp: {
            conf: "LtpSrl",
            input: { sents: ["他叫汤姆去拿外衣。"] }
            },
        ltp2: {
            conf: "LtpSrl2",
            input: { sents: ["他叫汤姆去拿外衣。", "安装LTP是非常简单的"] }
            },
    }
}
