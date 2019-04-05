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

        self.logger = u.new_logger(file, f'.logs/{file}.txt').thisClassLogger(self, "main")
        l = p.get("log", [])
        if len(l): self.logger.setLevel(l.pop(0))
        for k in l: self.logger.accept(k)

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
        print("received ws  from: ", name, "msg type=", msg.type)

    async def serve_ws(self, url, name):
        print(name, ":  connecting to: ", url)
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
        print("send_update is not implemented !")

    async def _get_exchange_updates(self):
        await self._register_competitor()
        while len(self.connections.keys()) < len(self.p["connect_to"]):
            await asyncio.sleep(0.1) # wait for all connections to start

        i=0; req = GetExchangeUpdateRequest(competitor_identifier=self._comp_id)
        async for exchange_update_response in self._stub.GetExchangeUpdate(req):
            try:
                # i+=1;
                # print("============================== i ================================")
                # print(exchange_update_response)
                # if i> 20: raise ValueError("couocu")
                i+=1;
                await asyncio.sleep(self.rtt/2)
                await self.send_exchange_updates(i, exchange_update_response)
            except Exception as e:
                self.fatal(e)
                print("ess traceback")
                traceback.print_exc()
            await asyncio.sleep(self.slowdown)
