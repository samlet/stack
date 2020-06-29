def depp_vis():
    from sagas.listings.dependency.biaffine_depp import DeppVisualizer
    import sagas
    r = sagas.profs.depp.BiaffineDepp(sentence="Hugging Face is a technology company based in New York and Paris")
    DeppVisualizer().render(r['data'])

if __name__ == '__main__':
    depp_vis()
