from process import Process
import random

class Network:
    def populate(self, population, min_id = None, max_id = None):
        Network.nodes = []
        
        if min_id is None or max_id is None:
            min_id = 1
            max_id = population
        else:
            if min_id > max_id:
                min_id, max_id = max_id, min_id
            
            if population < max_id - min_id + 1:
                population = max_id - min_id + 1
            
        for i in range(population):
            process = Process(random.randint(min_id, max_id))
            
            Network.nodes.append(process)
    
    nodes = []