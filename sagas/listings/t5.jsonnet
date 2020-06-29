{
    // sagas.profs.t5.T5_de(sentence='Hugging Face is a technology company')
    T5_de: {
        'type': 'sagas.listings.translation.t5_co.T5Co',
        'prefix': 'translate English to German'
    },
    // sagas.profs.t5.T5_fr(sentence='Hugging Face is a technology company')
    T5_fr: {
        'type': 'sagas.listings.translation.t5_co.T5Co',
        'prefix': 'translate English to French'
    },

    Examples: {
        de: {
            conf: "T5_de",
            input: { sentence: "Hugging Face is a technology company based in New York and Paris" }
            },
        fr: {
            conf: "T5_fr",
            input: { sentence: "Hugging Face is a technology company based in New York and Paris" }
            }
    }
}
