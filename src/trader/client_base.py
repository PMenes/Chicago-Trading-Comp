from aiogrpc import insecure_channel
import asyncio
import aiohttp
import time

from exchange.protos.service_pb2 import GetExchangeUpdateRequest
from exchange.protos.service_pb2_grpc import ExchangeServiceStub
import src.utils as u

class BaseExchangeGrpcClient():
    def __init__(self, file):
        self.c = c = u.config; self.p = p = c["processes"][file]

        u.delfile(f'.logs/{file}.txt')
        self.logger = u.log = u.setLogger(p.get("loggers")).classFilter(self, "main")

        h = c["exchange"]; channel = insecure_channel('%s:%s' % (h["host"], h["port"]))
        self._stub = ExchangeServiceStub(channel)
        self.connections = {}
        self.slowdown = 0
        self.rtt = c["rtt"] # round-trip time

    def start(self):
        tasks = []
        tasks.append([self._get_exchange_updates])
        for n in self.p["connect_to"]:
            h = self.c["processes"][n]; tasks.append([self.serve_ws, f'http://{h["host"]}:{h["port"]}/ws', n])
        return tasks

    async def stop(self):
        for k,v in self.connections.items(): await v["session"].close()

    async def handle_recvd(self, msg, name):
        self.debug("received ws  from: ", name, "msg type=", msg.type)

    async def serve_ws(self, url, name):
        self.info(name, ":  connecting to: ", url)
        session = aiohttp.ClientSession()
        try:
            async with session.ws_connect(url) as ws:
                c = self.connections[name] = {"session":session}
                c["ws"] = ws; await ws.send_str("iam=market_maker", False)
                async for msg in ws:
                    await self.handle_recvd(msg, name)
        except Exception as e:
            self.warning("closing...")
            await asyncio.sleep(0.3)
            await session.close()

    async def send_exchange_updates(self, num, upd):
        self.fatal("send_update is not implemented !")

    async def _get_exchange_updates(self):
        await self._register_competitor()
        while len(self.connections.keys()) < len(self.p["connect_to"]):
            await asyncio.sleep(0.1) # wait for all connections to start

        i=0; self.live = []; next_cycle = self.traderCycle(self)
        req = GetExchangeUpdateRequest(competitor_identifier=self._comp_id)
        async for upd in self._stub.GetExchangeUpdate(req):
            if not len(self.live):
                cycle = u.push(self.live, next_cycle)
                await cycle.process(i, upd)
                next_cycle = self.traderCycle(self)
            i += 1
            # i += 1
            # try:
            #     await self.send_exchange_updates(i, exchange_update_response)
            # except Exception as e:
            #     pass
            #     # self.error(e)
            # await asyncio.sleep(self.slowdown)
