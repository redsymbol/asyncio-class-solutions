import asyncio
PORT = 4242
NUM_CLIENTS = 0
def client_done(future):
    global NUM_CLIENTS
    NUM_CLIENTS += 1
    print('Client done')

def client_connected_handler(client_reader, client_writer):
    task = asyncio.Task(handle_client(client_reader, client_writer))
    task.add_done_callback(client_done)

@asyncio.coroutine
def handle_client(client_reader, client_writer):
    print('New client')
    while not client_reader.at_eof():
        data = (yield from client_reader.readline())
        print(data)
        client_writer.write(b'echo:' + data)

loop = asyncio.get_event_loop()
pending_server = asyncio.start_server(client_connected_handler, 'localhost', PORT)
server = loop.run_until_complete(pending_server)
try:
    loop.run_forever()
except KeyboardInterrupt:
    print('\n{} Clients Served'.format(NUM_CLIENTS))
finally:
    loop.close()
