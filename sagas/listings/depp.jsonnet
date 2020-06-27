{
    BiaffineDepp: {
        'type': 'sagas.listings.dependency.biaffine_depp.BiaffineDeppCo',
        'model': ''
    },

    Examples: {
        // $ list depp basic
        basic: {
            conf: "BiaffineDepp",
            visualizer: 'sagas.listings.dependency.biaffine_depp.DeppVisualizer',
            input: { sentence: "Hugging Face is a technology company based in New York and Paris" }
            }
    }
}
