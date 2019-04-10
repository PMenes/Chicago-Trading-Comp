import asyncio
from exchange.protos.order_book_pb2 import Order
from exchange.protos.service_pb2 import (
    RegisterCompetitorRequest,
    RegisterCompetitorResponse,
    CompetitorIdentifier,
    GetCompetitorMetadataRequest,
    PlaceOrderRequest,
    CancelOrderRequest,
    ModifyOrderRequest
)

from src.trader.client_base import BaseExchangeGrpcClient

class SendExchangeGrpcClient(BaseExchangeGrpcClient):
    def __init__(self, file):
        BaseExchangeGrpcClient.__init__(self, file)
        p = self.p
        self._comp_id = CompetitorIdentifier(competitor_id = p["client_id"], competitor_private_key = p["client_pk"])

    async def get_competitor_metadata(self):
        """Gets competitor metadata for this both
        @return GetCompetitorMetadataResponse
        """
        return await self._stub.GetCompetitorMetadata(GetCompetitorMetadataRequest(
            competitor_identifier = self._comp_id
        ))

    async def place_order(self, order: Order):
        try:
            x= await self._stub.PlaceOrder(PlaceOrderRequest(competitor_identifier=self._comp_id, order=order))
        except Exception as e:
            x= e
        await asyncio.sleep(self.rtt/2)
        return x

    async def modify_order(self, order_id: str, new_order: Order):
        try:
            x= await self._stub.ModifyOrder(ModifyOrderRequest(competitor_identifier=self._comp_id, order_id=order_id, new_order=new_order))
        except Exception as e:
            x= e
        await asyncio.sleep(self.rtt/2)
        return x

    async def cancel_order(self, order_id):
        try:
            x= await self._stub.CancelOrder(CancelOrderRequest(competitor_identifier=self._comp_id, order_id=order_id))
        except Exception as e:
            x= e
        await asyncio.sleep(self.rtt/2)
        return x

    async def _register_competitor(self):
        await self._stub.RegisterCompetitor(RegisterCompetitorRequest(
            competitor_identifier = self._comp_id
        ))
