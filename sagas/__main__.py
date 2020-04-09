def main():
    import fire
    from sagas.sagas_cli import SagasCli
    from sagas.startup import startup

    startup.start()
    fire.Fire(SagasCli)

if __name__ == "__main__":
    main()

