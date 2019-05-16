import simpy
import random


class Packet:
    def __init__(self, id, time, size, src="a"):
        self.id = "Pckt" + str(id)
        self.time = time
        self.size = size
        self.src = src


class PacketGenerator:
    def __init__(self, env, name, packet_lim, arrival_rate):
        self.env = env
        self.name = name
        self.out = None
        self.packet_lim = packet_lim
        self.packet_num = 0
        self.arrival_rate = arrival_rate
        self.action = env.process(self.generate_packets())

    def generate_packets(self):
        while self.packet_num < self.packet_lim:
            yield self.env.timeout(self.arrival_rate)
            self.packet_num += 1
            packet = Packet(self.packet_num, self.env.now, self.random_packet_size(), src=self.name)
            self.out.put(packet)

    @staticmethod
    def random_packet_size():
        packet_size = random.randint(1, 100)
        return packet_size


class Monitor:
    def __init__(self, env, rec_arrivals=False, absolute_arrivals=False, rec_waits=True, debug=False, selector=None):
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
            if self.debug:
                print("Packet : " + pkt.id + " From : " + pkt.src)


class Node:
    def __init__(self, env, name, buffer_size, t_rate, debug=False):
        self.env = env
        self.name = name
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

    def run(self):
        while True:
            pkt = yield self.store.get()
            self.status = 1  # Make it busy status.
            yield self.env.timeout(pkt.size/self.t_rate)

            self.out.put(pkt)
            self.status = 0  # Make it idle status.
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





