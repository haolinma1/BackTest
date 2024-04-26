from multiprocessing import Process, Queue
import logging
import datetime
import sys
import asyncio
import signal
import logging
import os
from fetchdata import Data
queue = Queue()


instType, instId, channel= sys.argv[1].split(',')

stream = Data(queue=queue, instType=instType, instId=instId, channel=channel)


def writer_proc(queue, output):
    while True:
        data = queue.get()
        if data is None:
            break
        symbol, timestamp, message = data
        date = datetime.datetime.fromtimestamp(timestamp).strftime('%Y%m%d')
        try:
            with open(os.path.join(output, '%s_%s.dat' % (symbol, date)), 'a') as f:
                print("File path:", os.path.abspath(os.path.join(output, '%s_%s.dat' % (symbol, date))))
                message = str(message)
                f.write(str(timestamp))
                f.write(' ')
                f.write(message)
                f.write('\n')
        except Exception as e:
            logging.exception('Failed to write data.')

def shutdown():
    asyncio.create_task(stream.close())
    for task in asyncio.all_tasks():
        task.cancel()

async def main():
    logging.basicConfig(level=logging.DEBUG)
    writer_p = Process(target=writer_proc, args=(queue, sys.argv[2],))
    writer_p.start()
    try:
        while not stream.closed:
            await stream.connect()
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        pass
    finally: 
        queue.put(None)
        writer_p.join()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    # for Linux
    # loop.add_signal_handler(signal.SIGTERM, shutdown)
    # loop.add_signal_handler(signal.SIGINT, shutdown)
    loop.run_until_complete(main())