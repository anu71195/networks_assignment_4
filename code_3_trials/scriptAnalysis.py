
#!/usr/bin/env python

import dpkt
import socket
import sys

#Arguments to be taken from command line
RtsCtsThreshold = int(sys.argv[1])
#End of arguments to be taken from command line

f= open('/home/rahul/networklab/assign4/workspace/ns-allinone-3.26/ns-3.26/node-0-0.pcap', 'rb')
pcap = dpkt.pcap.Reader(f)
count = 0

client_nodes = 2
server_node = 1
#size_RTS = 20  #size of RTS packet is 20 bytes in our application problem
total_bytes_RTS = 0
total_bytes_CTS = 0
total_bytes_ACK = 0

total_bytes_TCPSeg = 0      #max packet size allowed over 802.11 is 536 bytes. packet get fragmented when packet size increases over 536 bytes. If fragmentation threshold is less than 536 bytes then extra bytes will be lost
total_bytes_TCPAck = 0

for ts, buf in pcap:
	count += 1
	if(count == 1):
		start_time = ts
	#ARP packets(size = 64 bytes) are ignored
	if(len(buf) == 64):
		print count,": ARP Packet--- Ignored"
		continue

	ip = dpkt.ieee80211.IEEE80211(buf)
	size_packet = len(buf)    #size of each packet


	#RTS packet
	if(ip.subtype == 11):
		total_bytes_RTS += size_packet
		print count,": RTS packet"
		continue
	#CTS PAcket
	if(ip.subtype == 12):
		total_bytes_CTS += size_packet
		print count,": CTS packet"
		continue

	#ACK Packet
	if(ip.subtype == 13):
		total_bytes_ACK += size_packet
		print count,": ACK packet"
		continue
	
	#TCP Segments and TCP acks
	try:
		sender = dpkt.ieee80211.IEEE80211.BlockAckReq(buf).seq  #gives the number of nodes which is sending a packet
	except:
		pass
	else:
		if((sender == 1) or (sender == 3)):
			total_bytes_TCPSeg += len(ip.data)
			print count,": TCP segment"
			continue
		if(sender == 2):
			total_bytes_TCPAck += len(ip.data)
			print count,": TCP segment"
			continue
		
f.close()
        
time_duration = ts - start_time
#print time_duration, " ", total_bytes_RTS," ", total_bytes_CTS," ", total_bytes_ACK
#average bandwidth of RTS, CTS, ACK
avgBandWidth_RTS = float(total_bytes_RTS/(client_nodes*time_duration))/1000     #bytes per sec per node
avgBandWidth_CTS = float(total_bytes_CTS/(client_nodes*time_duration))/1000 
avgBandWidth_ACK = float(total_bytes_ACK/((client_nodes+server_node)*time_duration) )/1000    #since ack is being sent by all the three nodes

avgBandWidth_TCPSeg = float(total_bytes_TCPSeg/(client_nodes*time_duration) )/1000 
avgBandWidth_TCPAck = float(total_bytes_TCPAck/(client_nodes*time_duration) )/1000 

print "Avg. Bandwidth of RTS: ", avgBandWidth_RTS ," KB/sec per node"
print "Avg. Bandwidth of CTS: ", avgBandWidth_CTS ," KB/sec per node"
print "Avg. Bandwidth of ACK: ", avgBandWidth_ACK ," KB/sec per node"
print "Avg. Bandwidth of TCP Segment: ", avgBandWidth_TCPSeg ," KB/sec per node"
print "Avg. Bandwidth of TCP Ack: ", avgBandWidth_TCPAck ," KB/sec per node"


#Writes to the file TcpSegmentBandwidth values

with open ('/home/rahul/networklab/assign4/workspace/plottingFiles/TcpSegmentBandwidth.dat','a+') as TcpSegmentBandwidth:
	TcpSegmentBandwidth.write("%d\t%f\n" % (RtsCtsThreshold,avgBandWidth_TCPSeg))
TcpSegmentBandwidth.close()
#End of writing for TcpAckBandwidth values

#Writes to the file TcpAckBandwidth values

with open ('/home/rahul/networklab/assign4/workspace/plottingFiles/TcpAckBandwidth.dat','a+') as TcpAckBandwidth:
	TcpAckBandwidth.write("%d\t%f\n" % (RtsCtsThreshold,avgBandWidth_TCPAck))
TcpAckBandwidth.close()
#End of writing for TcpAckBandwidth values

#Writes to the file RtsCtsAck values

with open ('/home/rahul/networklab/assign4/workspace/plottingFiles/RtsCtsAckBandwidth.dat','a+') as RtsCtsAckBandwidth:
	RtsCtsAckBandwidth.write("%d\t%f\t%f\t%f\n" % (RtsCtsThreshold,avgBandWidth_RTS, avgBandWidth_CTS,avgBandWidth_ACK))
RtsCtsAckBandwidth.close()
#End of writing for RtsCtsAck values



node1AckBytes =0;   #number of acknowledged bytes received by node 1
node3AckBytes =0;   #number of acknowledged bytes received by node 3

#reading trace.txt to find out the acknowledged bytes at each node
with open("/home/rahul/networklab/assign4/workspace/trace.txt", "r") as traceFile:
	for packet in traceFile:
		if "> 10.1.1.3" in packet :
			#print packet
			if "ack" in packet:
				ackStr = packet[packet.index("ack") + len("ack") :]
				#print ackStr
				node3AckBytes = float(ackStr[: ackStr.index(',')])
				#print ackValue
			else:
				continue
			
		elif "> 10.1.1.1" in packet :
			#print packet
			if "ack" in packet:
				ackStr = packet[packet.index("ack") + len("ack")+1 :]
				#print ackStr
				node1AckBytes = float(ackStr[: ackStr.index(',')])
				#print ackValue
			else:
				continue

		else:
			continue
			
traceFile.close()

TCPThroughputNode1 = float(node1AckBytes/time_duration)/1000
TCPThroughputNode3 = float(node3AckBytes/time_duration)/1000

print "TCP Throughput of Node 1: ", TCPThroughputNode1, " KB per sec"
print "TCP Throughput of Node 3: ", TCPThroughputNode3, " KB per sec"

#Writes to the file TcpThroughputNode values

with open ('/home/rahul/networklab/assign4/workspace/plottingFiles/TcpThroughputNode.dat','a+') as TcpThroughputNode:
	TcpThroughputNode.write("%d\t%f\t%f\n" % (RtsCtsThreshold,TCPThroughputNode1,TCPThroughputNode3))
TcpThroughputNode.close()
#End of writing for TcpThroughputNode values

'''
#ack bytes wasted due to collision ---  collison occurs when ack for sent packet is not received
def calcWasteBytes(seqStr):
	seqStart = float(seqStr[: seqStr.index(":")])
	seqEnd = float(seqStr[seqStr.index(":")+1 : ])
	return (seqEnd - seqStart ) 
			

prev_seq_str = ""
bytesWasted = 0
with open("/home/rahul/networklab/assign4/workspace/trace.txt", "r") as traceFile:
	for packet in traceFile:
		if "10.1.1.1"  in packet and "> 10.1.1.2" in packet and "seq" in packet:
			seqStr = packet[packet.index("seq") + len("seq")+1 :]
			curr_seq_str = seqStr[: seqStr.index(',')]
			if ":" not in curr_seq_str:
				continue
			#print curr_seq_str
			if curr_seq_str == prev_seq_str :
				bytesWasted += calcWasteBytes(curr_seq_str)
			prev_seq_str = curr_seq_str
			continue

		if "10.1.1.3"  in packet and "> 10.1.1.2" in packet and "seq" in packet:
			seqStr = packet[packet.index("seq") + len("seq")+1 :]
			curr_seq_str = seqStr[: seqStr.index(',')]
			if ":" not in curr_seq_str:
				continue
			#print curr_seq_str
			if curr_seq_str == prev_seq_str :
				bytesWasted += calcWasteBytes(curr_seq_str)
			prev_seq_str = curr_seq_str
			continue

traceFile.close()
'''
collisonBytes = total_bytes_TCPSeg - (node3AckBytes + node1AckBytes)

avgBandWidth_Collison = float(collisonBytes/(client_nodes*time_duration))/1000 
print "Average Bandwidth wasted due to collison: ", avgBandWidth_Collison, " KB/sec per node"

#Writes to the file collisionBandwidth values

with open ('/home/rahul/networklab/assign4/workspace/plottingFiles/collisionBandwidth.dat','a+') as collisionBandwidth:
	collisionBandwidth.write("%d\t%f\n" % (RtsCtsThreshold,avgBandWidth_Collison))
collisionBandwidth.close()
#End of writing for collisionBandwidth values


