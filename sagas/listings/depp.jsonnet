{
    // sagas.profs.depp.BiaffineDepp(sentence="Hugging Face is a technology company based in New York and Paris")
    BiaffineDepp: {
        type: 'sagas.listings.dependency.biaffine_depp.BiaffineDeppCo',
        visualizer: 'sagas.listings.dependency.biaffine_depp.DeppVisualizer',
    },

    Examples: {
        // $ list depp basic
        basic: {
            conf: "BiaffineDepp",
            input: { sentence: "Hugging Face is a technology company based in New York and Paris" }
            }
    }
}
