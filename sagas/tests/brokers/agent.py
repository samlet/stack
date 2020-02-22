"""
# $ faust -A sagas.tests.brokers.agent worker -l info
"""
# examples/agent.py
import faust

# The model describes the data sent to our agent,
# We will use a JSON serialized dictionary
# with two integer fields: a, and b.
class Add(faust.Record):
    a: int
    b: int

# Next, we create the Faust application object that
# configures our environment.
app = faust.App('agent-example')

# The Kafka topic used by our agent is named 'adding',
# and we specify that the values in this topic are of the Add model.
# (you can also specify the key_type if your topic uses keys).
topic = app.topic('adding', value_type=Add)

@app.agent(topic)
async def adding(stream):
    async for value in stream:
        # here we receive Add objects, add a + b.
        yield value.a + value.b

# ***********

# @app.command()
# async def send_value() -> None:
#     """
#     $ faust -A sagas.tests.brokers.agent send_value
#     :return:
#     """
#     print(await adding.ask(Add(a=4, b=4)))

# from faust.cli import argument, option
#
# @app.command(
#     argument('a', type=int, help='First number to add'),
#     argument('b', type=int, help='Second number to add')
# )
# async def send_value(a: int, b: int) -> None:
#     print(f'Sending Add({a}, {b})...')
#     print(await adding.ask(Add(a, b)))

# $ faust -A sagas.tests.brokers.agent send_value 4 8 --printit
# :param a:
# :param b:
# :param printit:
# :return:

