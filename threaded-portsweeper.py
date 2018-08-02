import socket
import ipaddress
from ipaddress import IPv4Address, IPv4Network
import threading
from queue import Queue

count = 0
iplist = []
iprange = input("Enter IP range to check: ").strip()
port = input("Enter port you want to check: ").strip()
numthreads = input("Enter the number of threads (For Mac, use a max of 250 unless you up the ulimit...on kali and most linux distros use a max of 1000 unless you up the ulimit): ").strip()
port2 = int(port)
outfile = open("outfile.txt","w")
def Connector(ip):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.6)
        result = sock.connect_ex((str(ip),port2))
        sock.close()
        if result == 0:
            print("\033[92mPort " + str(port2) + " OPEN on %s\033[0m" % str(ip))
            outfile.write("Port " + str(port2) + " OPEN on %s\n" % str(ip))
        
    except Exception as e:
        print(e)

def threader():
    while True:
        worker = q.get()
        Connector(worker)
        q.task_done()

q = Queue()

for ip in ipaddress.IPv4Network(iprange):
    count = count + 1
    iplist.append(str(ip))
    
for x in range(int(numthreads)):
    t = threading.Thread(target=threader)
    t.daemon = True
    t.start()

for worker in iplist:
    q.put(worker)

q.join()

outfile.close()
print("+"*40)
print("\033[92mDONE!\033[0m")
print("Data written to outfile.txt in the current directory")
print("+"*40)

