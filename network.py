from process import Process
from numpy import inf
import random

#================================================================================
class Network:    
#================================================================================
# Methods
    #----------------------------------------------------------------------------
    # - Network Constructor
    #----------------------------------------------------------------------------
    # * population : number of total nodes (processes) in the Network
    # * min_id : minimum value of the ID space
    # * max_id : maximum value of the ID space
    #----------------------------------------------------------------------------
    def __init__(self, population, min_id = None, max_id = None):
        self.nodes = {}
        
        if min_id is None or max_id is None:
            min_id = 1
            max_id = population
        else:            
            if population > max_id - min_id + 1:
                population = max_id - min_id + 1
            
        if population < 1:
            return False
            
        available_ids = range(min_id, max_id + 1)
        id_set = random.sample(available_ids, population)

        available_ids += [-inf, inf]

        for id in id_set:
            process = Process(id)
            left_and_right = random.sample([i for i in available_ids if i != id], 2)
            process.left = left_and_right[0]
            process.right = left_and_right[1]
            process.network = self

            self.nodes[id] = process
            
        self.linearization = id_set + [-inf, inf]
        self.linearization.sort()

    #----------------------------------------------------------------------------
    # - Send Message
    #----------------------------------------------------------------------------
    # * recipient : id of the process to deliver the message to
    # * message : message to be delivered
    #----------------------------------------------------------------------------
    def send(self, recipient, message):
        if recipient in self.nodes:
            self.nodes[recipient].deliver(message)

    #----------------------------------------------------------------------------
    # - Is Linearized
    #----------------------------------------------------------------------------
    def linearized(self):
        for prev,cur,next in zip(self.linearization[:-2], self.linearization[1:-1], self.linearization[2:]):
            if prev is not self.nodes[cur].declared_left: return False
            if next is not self.nodes[cur].declared_right: return False
            
        return True

# Members
    nodes = {}
    linearization = []
#================================================================================
