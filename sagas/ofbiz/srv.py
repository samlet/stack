import asyncio
from aiohttp import web

from sagas.hybrid.hybrid_srv import HybridServ
from sagas.ofbiz.routines import routines
# import sagas.ofbiz.rpc_artifacts as artifacts
import logging
import sys

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s | %(levelname)s : %(message)s',
                     level=logging.INFO, stream=sys.stdout)

if __name__ == "__main__":
    # start routines * 这个服务在production环境下应该在backend-cluster中运行
    loop = asyncio.get_event_loop()
    connection = loop.run_until_complete(routines())
    print(".. routines serve.")

    # start artifacts servant
    # artifacts.serve(False)

    # start http-gateway * 这个服务将与rabbitmq服务一起部署在cloud-vm上, 作为网关
    # 这个服务不应该直接访问backend-cluster中运行的ofbiz/bots/hyperledger等服务
    serv = HybridServ()
    web.run_app(serv.init(loop), port=8099)

    # try:
    #     loop.run_forever()
    # finally:
    #     loop.run_until_complete(connection.close())
    #     loop.shutdown_asyncgens()
