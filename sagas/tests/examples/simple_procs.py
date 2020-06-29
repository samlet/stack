def simple():
    import sagas
    r = sagas.profs.simple.Simple(sentence='Hugging Face is a technology company')
    print('1.', r)
    sagas.profs.local_mode()
    r = sagas.profs.simple.Simple(sentence='Hugging Face is a technology company')
    print('2.', r)

if __name__ == '__main__':
    simple()
