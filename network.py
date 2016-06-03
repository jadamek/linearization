from process import Process
import random

class Network:    
    def __init__(self, population, min_id = None, max_id = None):
        self.nodes = {}
        
        if min_id is None or max_id is None:
            min_id = 1
            max_id = population
        else:
            if min_id > max_id:
                min_id, max_id = max_id, min_id
            
            if population > max_id - min_id + 1:
                population = max_id - min_id + 1
            
        if population < 3:
            return False
            
        available_ids = range(min_id, max_id + 1)

        for i in range(population):
            id = random.choice(available_ids)
            available_ids.remove(id)
            
            process = Process(id)
            left_and_right = random.sample([i for i in range(min_id, max_id + 1) if i != id], 2)
            process.left = left_and_right[0]
            process.lower = left_and_right[0]
            process.right = left_and_right[1]
            process.higher = left_and_right[1]
            process.network = self

            self.nodes[id] = process
            
    def send(self, recipient, message):
        if recipient in self.nodes:
            self.nodes[recipient].deliver(message)

    nodes = {}