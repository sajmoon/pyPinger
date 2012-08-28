import os, re, threading, time
from optparse import OptionParser

lock = threading.Lock()

class IpCollection():
	def __init__(self):
		self.ConfirmedIps = []
	def add(self, ip):
		# Lock this down
		self.ConfirmedIps.append(ip)

	def printIp(self, ip):
		print str(ip)
	def printAll(self):
		map(self.printIp, self.ConfirmedIps)

class Pinger(threading.Thread):
	def __init__(self, ip_number, collection):
		threading.Thread.__init__(self)
		self.Ip = ip_number
		self.ips = collection
		self.done = False

	def run(self):
		isActive = True
		ping = os.popen("ping "+self.Ip,"r")
		received_packages = re.compile(r"Received = (\d)")
		timeout_pattern = re.compile(r"Request timed out.")
		host_not_found_pattern = re.compile(r"Ping request could not find host")
		while True:
			line = ping.readline()
			if not line: break
			r = re.findall(received_packages, line)
			timeout = re.findall(timeout_pattern, line)
			host_not_found = re.findall(host_not_found_pattern, line)
			if not timeout == []:
				isActive = False
				if Debugg == True: print "Status: Ip not active: " + str(self.Ip)
				break
			if not host_not_found == []:
				isActive = False
				if Debugg == True: print "Status: ip not active: " + str(self.Ip)
				break
			if not r == []: received = r[0]
		if isActive == True:
			lock.acquire()
			try:
				self.ips.add(str(self.Ip))
				print "Status: Found ip: "+str(self.Ip)
			finally:
				lock.release()
		else:
			print "Status: Failed ip:"+str(self.Ip)
		self.done = True

parser = OptionParser()
parser.add_option("-a", "--first-min", dest="firstmin", metavar="INT")
parser.add_option("-b", "--first-max", dest="firstmax", metavar="INT")
parser.add_option("-c", "--second-min", dest="secondmin", metavar="INT")
parser.add_option("-d", "--second-max", dest="secondmax", metavar="INT")
parser.add_option("-e", "--third-min", dest="thirdmin", metavar="INT")
parser.add_option("-f", "--third-max", dest="thirdmax", metavar="INT")
parser.add_option("-g", "--forth-min", dest="forthmin", metavar="INT")
parser.add_option("-i", "--forth-max", dest="forthmax", metavar="INT")

parser.add_option("-t", "--threads", dest="max_threads", metavar="INT")

(options, args) = parser.parse_args()
ips = IpCollection()

counter = 1
ip_1_min = 1
ip_2_min = 1
ip_3_min = 1
ip_4_min = 1

ip_1_max = 255
ip_2_max = 255
ip_3_max = 255
ip_4_max = 255

if options.firstmin != None:
	ip_1_min = int(options.firstmin)
ip_1 = ip_1_min

if options.secondmin != None:
	ip_2_min = int(options.secondmin)
ip_2 = ip_2_min

if options.thirdmin != None:
	ip_3_min = int(options.thirdmin)
ip_3 = ip_3_min

if options.forthmin != None:
	ip_4_min = int(options.forthmin)
ip_4 = ip_4_min

if options.firstmax != None:
	ip_1_max = int(options.firstmax)
if options.secondmax != None:
	ip_2_max = int(options.secondmax)
if options.thirdmax != None:
	ip_3_max = int(options.thirdmax)
if options.forthmax != None:
	ip_4_max = int(options.forthmax)

if options.max_threads != None:
	max_threads = int(options.max_threads)
else:
	max_threads = 3

max_ips = 255
start_ip = 0
threads = []
Debugg = False
while True:
	if len(threads)< max_threads:
		if Debugg == True:
			print "Start new thread:"
		ip_str = str(ip_1)+"."+str(ip_2)+"."+str(ip_3)+"."+str(ip_4)
		thread = Pinger(ip_str, ips)
		threads += [thread]
		thread.start()
		if ip_4 == ip_4_max:
			ip_4 = ip_4_min
			if ip_3 == ip_3_max:
				ip_3 = ip_3_min
				if ip_2 == ip_2_max:
					ip_2 = ip_2_min
					if ip_1 == ip_1_max:
						break
					else:
						ip_1 = ip_1 + 1
				else:
					ip_2 = ip_2 + 1
			else:
				ip_3 = ip_3 + 1
		else:
			ip_4 = ip_4 + 1

	else:
		if Debugg == True:
			print("Sleep awhile")
		time.sleep(1)
		for x in threads:
			if x.done == True:
				threads.remove(x)
			if Debugg == True:
				print "Clearing threads"
		if Debugg == True:
			print "Ip list so far:"
			ips.printAll()
for x in threads:
	x.join()	
print "\n\nFinal ip list:"
ips.printAll()
