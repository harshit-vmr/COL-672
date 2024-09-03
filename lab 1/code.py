import os
import matplotlib.pyplot as plot_graph

ip = input("Enter Domain Name: ")
prev_ip = "NOT"
intermediate_ip = "NA"
ttl = 1
hop = []
IP = []
c = True
while c == True:
    res = os.popen(f"ping {ip} -i {ttl} -n 1 -4").read()
    hop.append(ttl)
    ttl = ttl+1
    if "Request timed out" in res:
        IP.append(int('0'))
        print("Request timed out.")
    else:
        res = res.split("Reply from ")[1]
        intermediate_ip = res[:res.find(':')]
        print(intermediate_ip)
        if "Average" in res:
            rtt = res.split("Average =")[1][:-3]
            IP.append(int(rtt))
            c = False;
        else:
            res = os.popen(f"ping {intermediate_ip} -n 2 -4").read()
            if "Request timed out" in res:
                IP.append(int('0'))
            else:
                res = res.split("Average =")[1]
                rtt = res[:-3]
                IP.append(int(rtt))
            
plot_graph.plot(hop,IP)
plot_graph.xlabel('Hops')
plot_graph.ylabel('RTT')
plot_graph.show()
