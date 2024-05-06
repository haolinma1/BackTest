from multiprocessing import Process, Queue
import datetime
import sys
import asyncio
import signal
import logging
from datetime import datetime
import os
from fetchdata import Data
import dotenv
queue = Queue()
dotenv.load_dotenv()
# data_path is the path to store the data
data_path = os.getenv("DATA_PATH")
output_path = os.getenv("OUTPUT_PATH")

instType, instId, channel= sys.argv[1].split(',')

stream = Data(queue=queue, instType=instType, instId=instId, channel=channel)


def writer_proc(queue, output):
    while True:
        data = queue.get()
        if data is None:
            break
        symbol, message = data
        current_date = datetime.now().date()
        try:
            with open(os.path.join(output, '%s_%s_%s.dat' % (symbol, current_date,channel)), 'a') as f:
                message = str(message)
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
    writer_p = Process(target=writer_proc, args=(queue, output_path,))
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