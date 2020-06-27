{
    BertSrl: {
        'type': 'sagas.listings.srl.bert_srl_co.BertSrlCo',
        'model': ''
    },

    Examples: {
        // $ list srl basic
        basic: {
            conf: "BertSrl",
            input: { sentence: "Hugging Face is a technology company based in New York and Paris" }
            }
    }
}
