import socket
import json
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('192.168.1.42', 10082))
pos = "r"

while True:
    s.listen(2)
    conn, addr = s.accept()
    data = conn.recv(1024)
    rdata = json.loads(data)
    print(repr(addr) + repr(rdata) + repr(pos))
    if rdata[0] > 960 and rdata[0] != 1000:
        pos = 'r'
        s.sendto(data, ("192.168.1.61", 10082))
    if rdata[0] < -960 and rdata[0] != 1000:
        pos = 'l'
        s.sendto(data, ("192.168.1.42", 10082))
    conn.send(pos.encode())
