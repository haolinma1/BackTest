from multiprocessing import Process, Queue
import logging
import datetime
import sys
import asyncio
import signal
import os
from fetchdata import Data
queue = Queue()
stream = Data(queue, sys.argv[2].split(','))


def writer_proc(queue, output):
    while True:
        data = queue.get()
        if data is None:
            break
        symbol, timestamp, message = data
        date = datetime.datetime.fromtimestamp(timestamp).strftime('%Y%m%d')
        with open(os.path.join(output, '%s_%s.dat' % (symbol, date)), 'a') as f:
            f.write(str(int(timestamp * 1000000)))
            f.write(' ')
            f.write(message)
            f.write('\n')

def shutdown():
    asyncio.create_task(stream.close())

async def main():
    logging.basicConfig(level=logging.DEBUG)
    writer_p = Process(target=writer_proc, args=(queue, sys.argv[3],))
    writer_p.start()
    while not stream.closed:
        await stream.connect()
        await asyncio.sleep(1)  
    queue.put(None)
    writer_p.join()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGTERM, shutdown)
    loop.add_signal_handler(signal.SIGINT, shutdown)
    loop.run_until_complete(main())