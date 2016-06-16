import random
from numpy import inf
from action import *

#================================================================================
class Process:
#================================================================================
# Represents a single process or network node.
#================================================================================
# Methods
    #----------------------------------------------------------------------------
    # - Process Constructor
    #----------------------------------------------------------------------------
    # * id : unique process id (node id) within network
    #----------------------------------------------------------------------------
    def __init__(self, id):
        self.id = id
        self.left = -inf
        self.right = inf
        self.channel = []        
        self.actions_ = []    

    #----------------------------------------------------------------------------
    # - Deliver Message
    #----------------------------------------------------------------------------
    # * message : message to be successfully added to process's channel and
    #       eventually received.
    #----------------------------------------------------------------------------
    def deliver(self, message):
        self.channel.append(message)
        
    #----------------------------------------------------------------------------
    # - Receive Message
    #----------------------------------------------------------------------------
    def receive(self):
        # Non-FIFO - randomly choose a waiting message
        message = random.choice(self.channel)
        self.channel.remove(message)
        
        return message
        
    #----------------------------------------------------------------------------
    # - Send Message
    #----------------------------------------------------------------------------
    # * recipient : id of the process in the network to receive the message
    # * message : the message being sent
    #----------------------------------------------------------------------------
    def send(self, recipient, message):
        self.network.send(recipient, message)

    #----------------------------------------------------------------------------
    # - Execute an Enabled Action    
    #----------------------------------------------------------------------------
    def act(self):
        # "Non-deterministic" action execution
        try:
            chosen = random.choice([action for action in ACTIONS if action.guard(self)])
        except IndexError:
            return None

        chosen.command(self)
        return chosen.name

    #----------------------------------------------------------------------------
    # - An Action is Enabled
    #----------------------------------------------------------------------------
    def enabled(self):
        return any([action.guard(self) for action in ACTIONS])

    #----------------------------------------------------------------------------
    # - Represent as a String (Overload)
    #----------------------------------------------------------------------------
    def __str__(self):
        return "[id:"+str(self.id)+", l:"+str(self.left)+", r:"+str(self.right)+", cl:"+str(self.declared_left)+", cr:"+str(self.declared_right)+"]"

# Members    
    id = 0
    left = 0
    right = 0
    
    channel = []
    actions_ = []
    declared_left = None
    declared_right = None
    network = None
#================================================================================
