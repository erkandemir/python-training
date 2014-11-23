import optparse
from socket import *
from threading import *

screenLock = Semaphore(value = 1)

def connScan(targetHost, targetPort):
	try:
		print(targetHost)
		connSkt = socket(AF_INET, SOCK_STREAM)
		connSkt.connect((targetHost,targetPort))
		connSkt.send("Hello")

		results = connSkt.recv(100)
		screenLock.acquire()
		print("Port is open")
	except:
		screenLock.acquire()
		print("Port is closed")
	finally:
		screenLock.release()
		connSkt.close()

def portScan(tgtHost, tgtPorts):
	try:
		tgtIp = gethostbyname(tgtHost)
	except:
		print("Can't resolve the host")
		return

	try:

		tgtName = gethostbyaddr(tgtIp)
		print("\n scan results for " + tgtName)
	except:
		print("can't resolve from ip: " + tgtIp)

	setdefaulttimeout(1)
	for port in tgtPorts:
		t = Thread(target = connScan, args=(tgtName,int(port)))
		t.start()

def Main():
	parser = optparse.OptionParser("Send host with -H and port with -P")
	parser.add_option("-H", dest = "tgthost", type="string", \
		help="host")
	parser.add_option("-P", dest = "tgtPorts", type="string", \
		help="ports")
	(options,args) = parser.parse_args()

	if(options.tgthost == None) | (options.tgtPorts == None):
		print parser.usage
		exit(0)
	else:
		tgtHost = options.tgthost
		tgtPorts = str(options.tgtPorts).split(',')

		portScan(tgtHost,tgtPorts)

if __name__ == '__main__':
	Main()
