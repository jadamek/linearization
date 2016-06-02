import random
from numpy import inf

class Process:
    def __init__(self, id):
        self.id = id
        self.channel = []
        self.lower = None
        self.higher = None
        self.left = 0
        self.right = 0
    
    def deliver(self, message):
        self.channel.append(message)
        
    def receive(self):
        message = random.choice(self.channel)
        self.channel.pop(message)
        print message
        
    def send(self, recipient, message):
        Network.send(recipient, message)
    
    id = 0
    lower = 0
    higher = 0
    left = 0
    right = 0
    channel = []