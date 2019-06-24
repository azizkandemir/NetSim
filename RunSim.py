# from test import Disposer, PacketGenerator, Node
from Components import Monitor, PacketGenerator, Node, ComponentMonitor
import simpy
import numpy
import random
from operator import itemgetter


def dist(distribution, dist_rate=None, dist_max=None):
    if distribution == "Poisson":
        return numpy.random.poisson(dist_rate)
    elif distribution == "Exponential":
        return numpy.random.exponential(dist_rate)
    elif distribution == "Uniform":
        return numpy.random.uniform(dist_rate, dist_max)
        # return random.randint(1, 100)
    elif distribution == "Pareto":
        pass


def run(values):
    pg_list = values['packetGenerator']
    node_list = values['node']
    monitor_list = values['monitor']

    env = simpy.Environment()

    monitor_dict = {}
    pg_dict = {}
    node_dict = {}

    for monitor in monitor_list:
        monitorName = monitor['componentToMonitor']
        monitor_dict["{}".format(monitorName)] = Monitor(env)

    for pg in pg_list:
        pgName = pg['name']
        packetCreation = pg['packetNum']
        arrivalType = pg['arrivalType']
        arrivalRate = pg['arrivalRate']
        arrivalRateMax = pg['arrivalRateMax']
        sizeType = pg['sizeType']
        sizeRate = pg['sizeRate']
        sizeRateMax = pg['sizeRateMax']

        # pg_dict["".format(pgName)] = PacketGenerator(env, pgName, packetCreation, arrivalType, sizeType,
        #                                              arrival_dist=dist, size_dist=dist, arrival_max=arrivalRateMax,
        #                                              arrival_rate=arrivalRate, size_rate=sizeRate,
        #                                              size_max_rate=sizeRateMax)

        if arrivalType == "Uniform" and sizeType == "Uniform":
            pg_dict["{}".format(pgName)] = PacketGenerator(env, pgName, packetCreation, arrivalType, sizeType,
                                                         arrival_dist=dist, size_dist=dist, arrival_max=arrivalRateMax,
                                                         arrival_rate=arrivalRate, size_rate=sizeRate,
                                                         size_max_rate=sizeRateMax)

        elif arrivalType != "Uniform" and sizeType == "Uniform":
            pg_dict["{}".format(pgName)] = PacketGenerator(env, pgName, packetCreation, arrivalType, sizeType,
                                                         arrival_dist=dist, size_dist=dist,
                                                         arrival_rate=arrivalRate, size_rate=sizeRate,
                                                         size_max_rate=sizeRateMax)

        elif arrivalType == "Uniform" and sizeType != "Uniform":
            pg_dict["{}".format(pgName)] = PacketGenerator(env, pgName, packetCreation, arrivalType, sizeType,
                                                         arrival_dist=dist, size_dist=dist, arrival_max=arrivalRateMax,
                                                         arrival_rate=arrivalRate, size_rate=sizeRate)

        elif arrivalType != "Uniform" and sizeType != "Uniform":
            pg_dict["{}".format(pgName)] = PacketGenerator(env, pgName, packetCreation, arrivalType, sizeType,
                                                         arrival_dist=dist, size_dist=dist,
                                                         arrival_rate=arrivalRate, size_rate=sizeRate)

        # else:
        #     pg_dict["".format(pgName)] = PacketGenerator(env, pgName, packetCreation, arrivalType, sizeType, arrival_dist=dist, size_dist=dist, arrival_rate=arrivalRate, size_rate=sizeRate)

    for node in node_list:
        nodeName = node['name']
        bufferSize = node['bufferSize']
        transmissionRate = node['transmissionRate']
        source = node['source']

        node_dict["{}".format(nodeName)] = Node(env, nodeName, bufferSize, transmissionRate)

        ############## Creation order koy packetGenerator ve node için daha sonra bunları merge edip creation ordera göre sort et.
        ############## Büyük listeyi ilk elemandan başlayarak instanceları oluştur(PacketGenerator ve Node classlarıyla). Böylece simpy eventine sok sırayla.


# arrival_rate = 2
# packet_creation = 1000
#
#
# def selector(pkt):
#     return pkt.src == "pg1"
#
#
# env = simpy.Environment()
#
# ps1 = Monitor(env, debug=False, rec_arrivals=True, selector=selector)
# pg1 = PacketGenerator(env, "pg1", packet_creation, arrival_rate)
# n1 = Node(env, "n1", 10, 20, debug=False)
# n2 = Node(env, "n2", 10, 10, debug=False)
# n3 = Node(env, "n3", 3, 10, debug=False)
#
# pg1.out = n1
# n1.out = n2
# n2.out = n3
# n3.out = ps1
#
# node_list = [n1, n2, n3]
#
# env.run()
#
# print("Packets sent: {}".format(pg1.packet_num))
#
# for node in node_list:
#     print("{} Packets dropped at {}".format(node.packet_dropped, node.name))
#
# print("Packets received: {}".format(ps1.packets_rec))


def test(values):
    pg_list = values["packetGenerator"]
    node_list = values["node"]
    monitor_list = values['monitor']

    big_list = []

    for pg in pg_list:
        big_list.append(pg)

    for node in node_list:
        big_list.append(node)

    big_list = sorted(big_list, key=itemgetter('creationOrder'))

    monitor_dict = {}
    pg_dict = {}
    node_dict = {}

    env = simpy.Environment()

    for comp in big_list:
        if comp['componentType'] == "packetGenerator":
            pgName = comp['name']
            packetCreation = comp['packetNum']
            arrivalType = comp['arrivalType']
            arrivalRate = comp['arrivalRate']
            arrivalRateMax = comp['arrivalRateMax']
            sizeType = comp['sizeType']
            sizeRate = comp['sizeRate']
            sizeRateMax = comp['sizeRateMax']

            if arrivalType == "Uniform" and sizeType == "Uniform":
                pg_dict["{}".format(pgName)] = PacketGenerator(env, pgName, packetCreation, arrivalType, sizeType,
                                                             arrival_dist=dist, size_dist=dist,
                                                             arrival_max=arrivalRateMax,
                                                             arrival_rate=arrivalRate, size_rate=sizeRate,
                                                             size_max_rate=sizeRateMax)

            elif arrivalType != "Uniform" and sizeType == "Uniform":
                pg_dict["{}".format(pgName)] = PacketGenerator(env, pgName, packetCreation, arrivalType, sizeType,
                                                             arrival_dist=dist, size_dist=dist,
                                                             arrival_rate=arrivalRate, size_rate=sizeRate,
                                                             size_max_rate=sizeRateMax)

            elif arrivalType == "Uniform" and sizeType != "Uniform":
                pg_dict["{}".format(pgName)] = PacketGenerator(env, pgName, packetCreation, arrivalType, sizeType,
                                                             arrival_dist=dist, size_dist=dist,
                                                             arrival_max=arrivalRateMax,
                                                             arrival_rate=arrivalRate, size_rate=sizeRate)

            elif arrivalType != "Uniform" and sizeType != "Uniform":
                pg_dict["{}".format(pgName)] = PacketGenerator(env, pgName, packetCreation, arrivalType, sizeType,
                                                             arrival_dist=dist, size_dist=dist,
                                                             arrival_rate=arrivalRate, size_rate=sizeRate)
            # if arrivalType == "Uniform":
            #     pg_dict["{}".format(pgName)] = PacketGenerator(env, pgName, packetCreation, arrivalType, sizeType,
            #                                                  arrival_dist=dist, size_dist=dist,
            #                                                  arrival_max=arrivalRateMax, arrival_rate=arrivalRate,
            #                                                  size_rate=sizeRate, size_max_rate=sizeRateMax)
            # else:
            #     pg_dict["{}".format(pgName)] = PacketGenerator(env, pgName, packetCreation, arrivalType, sizeType,
            #                                                  arrival_dist=dist, size_dist=dist,
            #                                                  arrival_rate=arrivalRate, size_rate=sizeRate)

        elif comp['componentType'] == "Node":
            nodeName = comp['name']
            bufferSize = comp['bufferSize']
            transmissionRate = comp['transmissionRate']
            source = comp['source']

            node_dict["{}".format(nodeName)] = Node(env, nodeName, bufferSize, transmissionRate, source=source)

    for node in node_dict:
        try:
            # print(node_dict[node].name + "'s source is " + pg_dict[node_dict[node].source].name)
            pg_dict[node_dict[node].source].out = node_dict[node]
            # print(pg_dict[node_dict[node].source].name + "'s out is --> " + pg_dict[node_dict[node].source].out.name)
        except:
            # print(node_dict[node].name + "'s source is " + node_dict[node_dict[node].source].name)
            node_dict[node_dict[node].source].out = node_dict[node]
            # print(node_dict[node_dict[node].source].name + "'s out is --> " + node_dict[node_dict[node].source].out.name)

    systemMonitor = Monitor(env)

    node_dict[node_list[-1]['name']].out = systemMonitor

    env.run()
    print("Sim finished.")

    for monitor in monitor_list:

        monitorName = monitor['name']

        pgToMonitor = None
        nodeToMonitor = None

        try:
            pgToMonitor = pg_dict[monitor['componentToMonitor']]

        except:
            nodeToMonitor = node_dict[monitor['componentToMonitor']]

        recordArrival = monitor['recordArrival']
        recordWaiting = monitor['recordWaiting']
        debug = monitor['debug']

        monitor_dict["{}".format(monitorName)] = ComponentMonitor(env, component_pg=pgToMonitor, component_node=nodeToMonitor, debug=debug, rec_waits=recordWaiting, rec_arrivals=recordArrival)

    systemMonitor.results()

    return node_list