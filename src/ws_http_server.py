import asyncio
import aiohttp
from aiohttp import web
import weakref
import uvloop
uvloop.install()

import src.utils as u

class WsHttpServer():
    def __init__(self, opt):
        loop = asyncio.get_event_loop()
        app = web.Application(loop=loop)
        app['websockets'] = weakref.WeakSet()
        app.on_shutdown.append(self.on_shutdown)
        self.app = app; self.opt = opt; self.wscons = {}

    def start(self):
        self.app.add_routes([
            web.get('/ws', self.ws_handle),
            web.get('/', self.serve_index),
        ])
        self.app.router.add_static('/', path=self.opt['static_path'])
        print(f"======== Serving local on {u.MyAddr().local()}:{self.opt['port']} ========")
        print(f"======== Serving world on {u.MyAddr().real()}:{self.opt['port']} ========")
        web.run_app(self.app, port=self.opt["port"])

    def close(self):
        self.app.close()

    async def serve_index(self, request): # serve index.html when no path...
        file = f"{self.opt['static_path']}/index.html"
        try:
            return web.FileResponse(file)
        except Exception as e:
            print(f"Error: file {file} not found ?: {e}")

    async def http_handle(self, request): # ... else serve asked file
        return web.Response(text="Hello, " + request.match_info.get('name', "Anonymous"))

    async def handle_recvd(self, msg): # should be handled by YOUR program
        print("received (not handled !!!):", msg.type)

    async def ws_handle(self, request):
        h,p = request.transport.get_extra_info('peername')
        if h is None: return
        peer = f'{h}:{p}'
        if peer in self.wscons: return print(f'{peer} already connected!, Closing..')
        self.wscons[peer] = ws = web.WebSocketResponse()
        print(f"new connection from {peer}")
        await ws.prepare(request)
        request.app['websockets'].add(ws)
        ws["p"] = {"peer": peer, "request": request}

        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.ERROR:
                self.ws_close(ws, f'message exception {ws.exception()}')
            await self.handle_recvd(msg, ws)
        return self.ws_close(ws, "connection was cut")

    def ws_close(self, ws, reason="unknown"):
        ws["p"]["request"].app['websockets'].discard(ws)
        peer = ws["p"]["peer"]; self.wscons.pop(peer)
        print(f'connection from {peer} closed. Reason: {reason}')
        return ws

    async def on_shutdown(self, app):
        for ws in set(app['websockets']):
            await ws.close(code=aiohttp.WSCloseCode.GOING_AWAY,
                           message='Server shutdown')
