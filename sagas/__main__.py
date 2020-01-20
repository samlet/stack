def main():
    import fire
    from sagas.sagas_cli import SagasCli
    from sagas.tool.loggers import init_logger
    init_logger()
    fire.Fire(SagasCli)

if __name__ == "__main__":

    main()

