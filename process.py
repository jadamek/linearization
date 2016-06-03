import random
from numpy import inf

class Process:
    def __init__(self, id):
        self.id = id
        self.channel = []
        self.lower = -inf
        self.higher = inf
        self.left = -inf
        self.right = inf
    
    def deliver(self, message):
        self.channel.append(message)
        
    def receive(self):
        message = random.choice(self.channel)
        self.channel.pop(message)
        print message
        
    def send(self, recipient, message):
        network.send(recipient, message)
        
    def __str__(self):
        return "[id:"+str(self.id)+", l:"+str(self.lower)+", r:"+str(self.higher)+"]"
    
    id = 0
    lower = 0
    higher = 0
    left = 0
    right = 0
    channel = []
    network = None