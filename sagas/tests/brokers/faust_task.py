import faust

app = faust.App('myapp', broker='kafka://')

class AddOperation(faust.Record):
    x: int
    y: int

@app.agent()
async def add(stream):
    async for op in stream:
        yield op.x + op.y

@app.command()
async def produce():
    await add.send(value=AddOperation(2, 2))

if __name__ == '__main__':
    # $ faust -A sagas.tests.brokers.faust_task worker -l info
    # $ faust -A sagas.tests.brokers.faust_task produce
    app.main()
