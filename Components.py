import simpy
import random

total_packets = 0
total_drops = 0


class Packet:
    def __init__(self, id, time, size, src="a"):
        self.id = "Pckt" + str(id)
        self.time = time
        self.size = size
        self.src = src

        global total_packets
        total_packets += 1


class PacketGenerator:
    def __init__(self, env, name, packet_lim, arrival_dist_name, size_dist_name, size_max_rate=None, size_rate=None, arrival_max=None, arrival_rate=None, arrival_dist=None, size_dist=None):
        self.env = env
        self.name = name
        self.out = None
        self.packet_lim = packet_lim
        self.packet_num = 0

        self.arrival_dist = arrival_dist
        self.arrival_dist_name = arrival_dist_name
        self.arrival_rate = arrival_rate
        self.arrival_max = arrival_max

        self.size_dist = size_dist
        self.size_dist_name = size_dist_name
        self.size_max_rate = size_max_rate
        self.size_rate = size_rate

        self.action = env.process(self.generate_packets())

    def generate_packets(self):
        while self.packet_num < self.packet_lim:
            yield self.env.timeout(self.arrival_dist(self.arrival_dist_name, dist_rate=self.arrival_rate, dist_max=self.arrival_max))
            self.packet_num += 1
            packet = Packet(self.packet_num, self.env.now, self.random_packet_size(self.size_dist, self.size_dist_name, self.size_rate, self.size_max_rate), src=self.name)
            self.out.put(packet)

    @staticmethod
    def random_packet_size(dist_func, size_dist, size_rate, size_max_rate):
        # packet_size = random.randint(1, 100)
        packet_size = dist_func(size_dist, dist_rate=size_rate, dist_max=size_max_rate)
        return packet_size


class ComponentMonitor:
    def __init__(self, env, component_node=None, component_pg=None, rec_arrivals=False, rec_waits=False, debug=False):
        self.env = env
        self.packets_rec = 0
        self.pgToMonitor = component_pg
        self.nodeToMonitor = component_node
        self.debug = debug
        self.arrivals = []
        self.waits = []
        self.results = self.results()

        if self.nodeToMonitor:
            if self.debug:
                self.nodeToMonitor.debug = True

    def throughput(self):
        return self.nodeToMonitor.packet_received / self.nodeToMonitor.busy_time

    def results(self):
        if self.nodeToMonitor:
            print("Received Packets: " + str(self.nodeToMonitor.packet_received) + " Dropped Packets: " + str(self.nodeToMonitor.packet_dropped) + " Node: " + self.nodeToMonitor.name)
            print(self.nodeToMonitor.name, " Throughput: ", self.throughput(), "bytes/sec")
            print(self.nodeToMonitor.name, " Throughput: ", self.throughput()*8, "bits/sec")
        elif self.pgToMonitor:
            print("Created Packets: " + str(self.pgToMonitor.packet_num) + " Packet Generator: " + self.pgToMonitor.name)


class Monitor:
    def __init__(self, env, simulation_duration=None, rec_arrivals=True, absolute_arrivals=True, rec_waits=True, debug=False, selector=None):
        self.env = env
        self.packets_rec = 0
        self.last_arrival = 0.0
        self.arrivals = []
        self.rec_arrivals = rec_arrivals
        self.rec_waits = rec_waits
        self.absolute_arrivals = absolute_arrivals
        self.waits = []
        self.selector = selector
        self.debug = debug
        self.total_packets = 0
        self.total_drops = 0
        self.received_size = 0
        self.simulation_duration = simulation_duration

    def put(self, pkt):
        if not self.selector or self.selector(pkt):
            now = self.env.now
            if self.rec_waits:
                self.waits.append(self.env.now - pkt.time)
            if self.rec_arrivals:
                if self.absolute_arrivals:
                    self.arrivals.append(now)
                else:
                    self.arrivals.append(now - self.last_arrival)
                self.last_arrival = now

            self.packets_rec += 1
            self.received_size += pkt.size
            if self.debug:
                print("Packet : " + pkt.id + " From : " + pkt.src)

    def throughput(self):
        if self.simulation_duration:
            return self.received_size / self.simulation_duration
        else:
            return self.received_size / self.last_arrival

    def results(self):
        if self.rec_arrivals:
            print("Packets Received: ", len(self.arrivals))
            print("Packets Dropped: ", total_packets - len(self.arrivals))
        if self.rec_waits:
            print("Mean Waiting Time: ", sum(self.waits)/len(self.waits))

        print("System Throughput: ", self.throughput(), "byte/sec")
        print("System Throughput: ", self.throughput()*8, "bit/sec")


class Node:
    def __init__(self, env, name, buffer_size, t_rate, source=None, debug=False):
        self.env = env
        self.name = name
        self.source = source
        self.out = None
        self.status = None  # 1 for busy, 0 for idle.
        self.packet_received = 0
        self.store = simpy.Store(env)
        self.t_rate = t_rate
        self.action = env.process(self.run())
        self.packet_dropped = 0
        self.debug = debug
        self.buffer_size = buffer_size
        self.current_size = 0
        self.total_packets = 0
        self.total_drops = 0
        self.busy_time = 0

    def run(self):
        while True:
            pkt = yield self.store.get()
            self.status = 1  # Make it busy status.
            before = self.env.now
            yield self.env.timeout(pkt.size/self.t_rate)
            self.out.put(pkt)
            self.status = 0  # Make it idle status.
            after = self.env.now
            self.busy_time += after - before
            self.current_size -= 1

    def put(self, packet):
        self.packet_received += 1
        self.current_size += 1
        if self.buffer_size >= self.current_size:
            self.store.put(packet)
        else:
            if self.debug:
                print("Packet : " + packet.id + " From: " + packet.src + " Dropped at " + self.name + ".")
            self.packet_dropped += 1
            self.current_size -= 1
            global total_drops
            total_drops -= 1




