import json
import wave
import socket


with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    server_addr = ('127.0.0.1', 9999)
    buffer_size = 1024
    wf = wave.open('sample.wav', 'rb')
    params = wf.getparams()._asdict()
    params = json.dumps(params).encode()
    w_data = wf.readframes(buffer_size)
    sent_params = sock.sendto(params, server_addr)
    sent = sock.sendto(w_data, server_addr)

    while w_data != b'':
        w_data = wf.readframes(buffer_size)
        sent = sock.sendto(w_data, server_addr)
    sock.sendto(b'', server_addr)




