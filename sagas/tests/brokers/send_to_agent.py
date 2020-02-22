# examples/send_to_agent.py
import asyncio
from .agent import Add, adding

async def send_value() -> None:
    print(await adding.ask(Add(a=4, b=4)))

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_value())

# $ python -m sagas.tests.brokers.send_to_agent

