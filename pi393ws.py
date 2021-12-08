#
#	Control Vex 393 motors with websockets
#	Based on my pi_vex_393 library
#
#

# imports
from asyncio.events import get_event_loop
import websockets
from websockets import WebSocketServerProtocol
import asyncio


# pasted from medium, need to make this work
class Server:
	clients = set()

	async def register(self, ws: WebSocketServerProtocol) -> None:
		self.clients.add(ws)
		print(f'Add client: {ws.remote_address}')

	async def unregister(self, ws: WebSocketServerProtocol) -> None:
		self.clients.remove(ws)
		print(f'Remove client: {ws.remote_address}')

	async def broadcast(self, message: str) -> None:
		if self.clients:
			await asyncio.wait([client.send(message) for client in self.clients])

	async def handle(self, ws: WebSocketServerProtocol, path: str) -> None:
		await self.register(ws)
		try:
			await self.distribute(ws, path)
		finally:
			await self.unregister(ws)

	async def distribute(self, ws: WebSocketServerProtocol) -> None:
		async for message in ws:
			await self.broadcast(message)

