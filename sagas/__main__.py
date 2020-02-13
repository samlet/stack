def main():
    import fire
    from sagas.sagas_cli import SagasCli
    from sagas.tool.loggers import init_logger
    from sagas.startup import startup

    init_logger()
    startup.start()

    fire.Fire(SagasCli)

if __name__ == "__main__":

    main()

