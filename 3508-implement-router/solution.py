import random
from bisect import bisect_left, bisect_right
from collections import deque
import time

class Router(object):

    def __init__(self, memoryLimit):
        """
        :type memoryLimit: int
        """
        self.memory_limit = memoryLimit
        self.packet_queue = deque()
        self.destination_map = dict()
        self.packet_set = set()
        

    def addPacket(self, source, destination, timestamp):
        """
        :type source: int
        :type destination: int
        :type timestamp: int
        :rtype: bool
        """

        if (source, destination, timestamp) in self.packet_set:
            return False
        
        if destination not in self.destination_map:
            self.destination_map[destination] = [0, list()] # [start-index, list of timestamps]
        
        if len(self.packet_queue) >= self.memory_limit: 
            old_packet = self.packet_queue.popleft()
            self.destination_map[old_packet[1]][0] += 1
            self.packet_set.remove(tuple(old_packet))

        self.packet_queue.append([source, destination, timestamp])
        self.packet_set.add((source, destination, timestamp))
        self.destination_map[destination][1].append(timestamp)
        return True

        

    def forwardPacket(self):
        """
        :rtype: List[int]
        """
        if self.packet_queue:
            forwarded = self.packet_queue.popleft()
            self.destination_map[forwarded[1]][0] += 1
            self.packet_set.remove(tuple(forwarded))
            return forwarded
        return []
        

    def getCount(self, destination, startTime, endTime):
        """
        :type destination: int
        :type startTime: int
        :type endTime: int
        :rtype: int
        """
        if destination not in self.destination_map:
            return 0

        timestamps_removed = self.destination_map[destination][0]
        timestamp_list = self.destination_map[destination][1]

        if timestamp_list:
            first_index = bisect_left(timestamp_list, startTime, lo=timestamps_removed)
            last_index = bisect_right(timestamp_list, endTime, lo=timestamps_removed)
            return last_index-first_index
        return 0



# Basic tests for debugging; not relevant for LeetCode submission
if __name__ == "__main__":

    random.seed(42)
    start_time = time.time()
    timestamp = 1
    obj = Router(100000)

    actions = 0
    for i in range(10**6):
        if random.random() < 0.5:
            actions += 1
            source = random.randint(1,10**5)
            destination = random.randint(1,10**5)
            timestamp = timestamp + random.randint(0,100)
            addPacket_return = obj.addPacket(source,destination,timestamp)
            # print(f"Add packet: {[source, destination, timestamp]}, Status {addPacket_return}")
            # print(addPacket_return)

        if random.random() < 0.3:
            actions += 1
            forwardPacket_return = obj.forwardPacket()
            # print(f"Forward packet: {forwardPacket_return}")

        if random.random() < 0.3:
            actions += 1
            getCount_return = obj.getCount(4,10,39)
            # print(f"Count: {getCount_return}")
        # print(f"Object queue: {obj.packet_queue}\n")

    print(time.time()-start_time)
    print(actions)