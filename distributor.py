from src.ws_http_server import WsHttpServer
import src.utils as u
from config import config

class Distributor(WsHttpServer):
    def __init__(self):
        self.config = c = config
        self.mmset = 0
        WsHttpServer.__init__(self, c["processes"][__file__])

    def start(self):
        self.app.router.add_static('/get', path=self.opt['get_path'])
        super().start()

    async def handle_recvd(self, msg, ws):
        m = msg.data; wis = ws["p"].get("iam", 0)
        if m[:4] == "iam=":
            await self.init_connection(m[4:], ws)
        else:
            await self.distribute_message(ws["p"].get("iam", 0), m)

    async def init_connection(self, wis, ws):
        ws["p"]["iam"] = wis
        if wis == "market_maker":
            if self.mmset: return self.ws_close(ws, "too many mms!") # only one mm !!
            self.mmset = 1
        if wis[:6] == "client":
            await ws.send_json({"action": "init", "data": self.config})
        print(f"connection is: {wis}")

    async def distribute_message(self, wis, m):
        if not wis: return
        if wis == "market_maker": # then distribute to all connected clients
            for k in self.wscons:
                w = self.wscons[k]; cwis = w["p"].get("iam",0)
                try:
                    if cwis[:6] == "client": await w.send_str(m)
                except Exception as e:
                    print("Error sending", e)

if __name__ == "__main__":
    u.launch_server(Distributor)
