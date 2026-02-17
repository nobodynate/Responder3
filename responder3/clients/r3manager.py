#!/usr/bin/env python3.6
import asyncio
from responder3.core.commons import *
from responder3.protocols.R3M import *


class R3ManagerClient:
	def __init__(self, loop):
		self.loop = loop
		self.host = '127.0.0.1'
		self.port = 55551
		self.ssl_ctx = None

	async def connect_responder(self):
		self.reader, self.writer = await asyncio.open_connection(self.host, self.port, loop=self.loop)

	async def send_command(self, cmd):
		self.writer.write(cmd.to_bytes())
		await self.writer.drain()
		return await Responder3Command.from_streamreader(self.reader)

	async def main(self):
		cmd = R3ServerListCommand()
		await self.connect_responder()
		await self.send_command(cmd)

async def _async_main():
	client = R3ManagerClient(asyncio.get_running_loop())
	await client.main()

def main():
	asyncio.run(_async_main())

if __name__ == '__main__':
	main()
