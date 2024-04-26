import time
import asyncio
import json
import logging
import aiohttp



class Data:
    def __init__(self, queue, instType, instId, channel, timeout=7):
        """_summary_

        Args:
            queue (_type_): _description_
            instType (string): used to specify the trade type, etc: USDT-FUTURES, SPOT 
            instId (string): the symbol, etc: ETHUSDT, BTCUSDT
            channel (string): specify the market data to fetch, etc: trade - public trade, books5- market order
            timeout (int, optional): _description_. Defaults to 7.
        """
        self.instType = instType
        self.client = aiohttp.ClientSession(
            headers={'Content-Type': 'application/json'})
        self.closed = False
        self.pending_messages = {}
        self.prev_u = {}
        self.timeout = timeout
        self.keep_alive = None
        self.queue = queue
        self.channel = channel
        self.instId = instId

    async def __on_message(self, raw_message):
        timestamp = time.time()
        message = json.loads(raw_message)
        logging.debug(message)

    async def __keep_alive(self):
        while not self.closed:
            try:
                await asyncio.sleep(5)
                await self.ws.pong()
            except asyncio.CancelledError:
                return
            except:
                logging.exception('Failed to keep alive.')
                return

    async def close(self):
        self.closed = True
        await self.ws.close()
        await self.client.close()
        await asyncio.sleep(1)

    async def connect(self):
        try:
            baseURL = 'wss://ws.bitget.com/v2/ws/public'
            send_message = {
                "op": "subscribe",
                "args": [
                    {
                        "instType": f'{self.instType}',
                        "channel": f'{self.channel}',
                        "instId": f'{self.instId}'
                    }
                ]
            }
            async with aiohttp.ClientSession() as session:
                async with session.ws_connect(baseURL) as ws:
                    await ws.send_json(send_message)
                    logging.info('WS Connected.')
                    self.keep_alive = asyncio.create_task(self.__keep_alive())
                    async for msg in ws:
                        if msg.type==aiohttp.WSMsgType.TEXT:
                            await self.__on_message(msg.data) 
                        elif msg.type == aiohttp.WSMsgType.PING:
                            await self.ws.pong()
                        elif msg.type == aiohttp.WSMsgType.PONG:
                            await self.ws.ping()
                        elif msg.type == aiohttp.WSMsgType.ERROR:
                            exc = ws.exception()
                            raise exc if exc is not None else Exception
        except:
            logging.exception('WS Error')

        finally:
            logging.info('WS Disconnected')
            if self.keep_alive is not None:
                self.keep_alive.cancel()
                await self.keep_alive
            self.ws = None
            self.keep_alive = None



