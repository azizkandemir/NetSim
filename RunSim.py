# from test import Disposer, PacketGenerator, Node
from Components import Monitor, PacketGenerator, Node
import simpy


arrival_rate = 2
packet_creation = 1000


def selector(pkt):
    return pkt.src == "pg1"


env = simpy.Environment()

ps1 = Monitor(env, debug=False, rec_arrivals=True, selector=selector)
pg1 = PacketGenerator(env, "pg1", packet_creation, arrival_rate)
n1 = Node(env, "n1", 10, 20, debug=False)
n2 = Node(env, "n2", 10, 10, debug=False)
n3 = Node(env, "n3", 3, 10, debug=False)

pg1.out = n1
n1.out = n2
n2.out = n3
n3.out = ps1

node_list = [n1, n2, n3]


env.run()

print("Packets sent: {}".format(pg1.packet_num))

for node in node_list:
    print("{} Packets dropped at {}".format(node.packet_dropped, node.name))

print("Packets received: {}".format(ps1.packets_rec))
