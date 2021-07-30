import asyncio
import time
import wave
import json


async def write_to_file_from_queue(wf, queue):
    while True:
        try:
            item = await asyncio.wait_for(queue.get(), 3)
        except asyncio.TimeoutError:
            print('conn close')
            wf.close()
            break
        if item == b'':
            print('and of queue')
            wf.close()
            break
        else:
            wf.writeframes(item)



class EchoServerProtocol:
    queues = {}

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        print('Received %r from %s' % (len(data), addr))
        if addr not in self.queues:
            filename = str(time.time())
            wf = wave.open(filename, 'wb')
            params = json.loads(data.decode())
            params = (params['nchannels'], params['sampwidth'], params['framerate'], params['nframes'], params['comptype'], params['compname'])
            wf.setparams(params)
            self.queues[addr] = asyncio.Queue()
            asyncio.create_task(write_to_file_from_queue(wf, self.queues[addr]))
        else:
            self.queues[addr].put_nowait(data)


async def main():
    print("Starting UDP server")
    loop = asyncio.get_running_loop()
    transport, protocol = await loop.create_datagram_endpoint(
        EchoServerProtocol,
        local_addr=('127.0.0.1', 9999))
    try:
        await asyncio.sleep(3600)
    finally:
        transport.close()

asyncio.run(main())