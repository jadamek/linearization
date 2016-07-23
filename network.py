from process import Process
from numpy import inf
import random
import sys
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
        
        if min_id == None or max_id == None:
            min_id = 1
            max_id = population
        else:            
            if population > max_id - min_id + 1:
                population = max_id - min_id + 1
            
        if population < 1:
            return False

        self.min_id = min_id
        self.max_id = max_id
            
        available_ids = range(min_id, max_id + 1)
        id_set = random.sample(available_ids, population)
        
        self.linearization = id_set + [-inf, inf]
        self.linearization.sort()

        for prev,cur,next in zip(self.linearization[:-2], self.linearization[1:-1], self.linearization[2:]):
            process = Process(cur)
            process.left = prev
            process.declared_left = prev
            process.right = next
            process.declared_right = next
            process.network = self

            self.nodes[cur] = process
                       
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
    # - Randomly Perturb Processes
    #----------------------------------------------------------------------------
    # * errors : number of processes to randomly perturb, setting an arbitrary
    #       neighbor state.
    #----------------------------------------------------------------------------
    def perturb(self, errors):
        if errors > len(self.nodes): errors = len(self.nodes)
                
        perturbed_ids = random.sample(self.linearization[1:-1], errors)
        
        for id in perturbed_ids:
            # Real IDs Only
            #self.nodes[id].left = random.choice([i for i in self.linearization if i < id])
            #self.nodes[id].right = random.choice([i for i in self.linearization if i > id])

            # Fake IDs        
            self.nodes[id].left = random.choice(range(self.min_id, id) + [-inf])
            self.nodes[id].right = random.choice(range(id + 1, self.max_id) + [inf])
            #print "perturbed %f with l:%f and r:%f" % (id, self.nodes[id].left, self.nodes[id].right)
            #sys.stdout.flush()
    #----------------------------------------------------------------------------
    # - Is Linearized
    #----------------------------------------------------------------------------
    def linearized(self):
        for i in range(1, len(self.linearization) - 1):
            if self.nodes[self.linearization[i]].left != self.linearization[i - 1]:
                return False
            if self.nodes[self.linearization[i]].right != self.linearization[i + 1]:
                return False
            
        return True

# Members
    nodes = {}
    linearization = []
    min_id = 0
    max_id = 1
#================================================================================
