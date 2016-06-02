from process import Process
import random

class Network:
    def populate(self, population, min_id = None, max_id = None):
        Network.nodes = {}
        
        if min_id is None or max_id is None:
            min_id = 1
            max_id = population
        else:
            if min_id > max_id:
                min_id, max_id = max_id, min_id
            
            if population < max_id - min_id + 1:
                population = max_id - min_id + 1
            
        if population < 3:
            return False
            
        available_ids = range(min_id, max_id + 1)

        for i in range(population):
            id = random.choice(available_ids)
            available_ids.pop(id)
            
            process = Process(id)
            left_and_right = random.sample(range(min_id, max_id + 1) - process.id, 2)
            process.left = left_and_right[0]
            process.left = left_and_right[1]

            Network.nodes[id] = process
            
    def send(self, recipient, message):
        if recipient in Network.nodes:
            network.nodes[recipient].deliver(message)

    nodes = {}