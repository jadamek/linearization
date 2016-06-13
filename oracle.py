from numpy import inf
from message import Message
import random

#================================================================================
class OracleWC:
#================================================================================
# Represents the Weak Connectivity Oracle, which repairs any network disjunctions
#================================================================================
# Methods
    #----------------------------------------------------------------------------
    # - Oracle Constructor
    #----------------------------------------------------------------------------
    def __init__(self):
        self.executions = 0

    #----------------------------------------------------------------------------
    # - Check Guard
    #----------------------------------------------------------------------------
    # * network : network to evaluate the oracles's action's guard against
    #----------------------------------------------------------------------------
    def guard(self, network):
        remaining = set(network.nodes.keys())
        component = self.compute_component(network.nodes[1].id, set([]), remaining, network)
        
        matched = True
        while matched:
            matched = False
            for id in remaining:
                if network.nodes[id].left in component or network.nodes[id].right in component or len(component.intersection(set([message.content for message in network.nodes[id].channel]))) > 0:
                    self.compute_component(id, component, remaining, network)
                    matched = True
                    break

        return len(remaining) > 0
    
    #----------------------------------------------------------------------------
    # - Execute Command
    #----------------------------------------------------------------------------
    # * network : network to execute the oracle's action on
    #----------------------------------------------------------------------------
    def command(self, network):
        remaining = set(network.nodes.keys())
        component = self.compute_component(network.nodes[1].id, set([]), remaining, network)
        
        matched = True
        while matched:
            matched = False
            for id in remaining:
                if network.nodes[id].left in component or network.nodes[id].right in component or len(component.intersection(set([message.content for message in network.nodes[id].channel]))) > 0:
                    self.compute_component(id, component, remaining, network)
                    matched = True
                    break

        icebreaker = random.choice(tuple(component))
        network.nodes[icebreaker].send(random.choice(tuple(remaining)), Message(icebreaker))

        self.executions += 1

    #----------------------------------------------------------------------------
    # - Compute Forward Component (private)
    #----------------------------------------------------------------------------
    # * id : the ID of the current process being discovered in the component
    # * component : list of processes that belong to the current component
    # * remaining : list of processes that do not yet belong to the component
    # * network : network this component belongs to
    #----------------------------------------------------------------------------
    def compute_component(self, id, component, remaining, network):        
        process = network.nodes[id]
        component.add(id)
        remaining.remove(id)

        if process.left not in component | set([-inf, inf]):
            self.compute_component(process.left, component, remaining, network)
        if process.right not in component | set([-inf, inf]):
            self.compute_component(process.right, component, remaining, network)

        for message in process.channel:
            if message.content not in component | set([-inf, inf]):
                self.compute_component(message.content, component, remaining, network)

        return component
        
# Members
    name = "WC"
    executions = 0
#================================================================================

#================================================================================
class OraclePD:
#================================================================================
# Represents the Participant Detector Oracle, which removes non-existant IDs from
# any process's records
#================================================================================
# Methods
    #----------------------------------------------------------------------------
    # - Oracle Constructor
    #----------------------------------------------------------------------------
    def __init__(self):
        self.executions = 0

    #----------------------------------------------------------------------------
    # - Check Guard
    #----------------------------------------------------------------------------
    # * network : network to evaluate the oracles's action's guard against
    #----------------------------------------------------------------------------
    def guard(self, network):
        for pid in network.nodes:
            if network.nodes[pid].left not in network.linearization:
                return True
            if network.nodes[pid].right not in network.linearization:
                return True
        return False
    
    #----------------------------------------------------------------------------
    # - Execute Command
    #----------------------------------------------------------------------------
    # * network : network to execute the oracle's action on
    #----------------------------------------------------------------------------
    def command(self, network):
        for pid in network.nodes:
            if network.nodes[pid].left not in network.linearization:
                network.nodes[pid].left = -inf
                break
            if network.nodes[pid].right not in network.linearization:
                network.nodes[pid].right = inf
                break
        self.executions += 1

# Members
    name = "PD"
    executions = 0
#================================================================================

#================================================================================
class OracleNO:
#================================================================================
# Represents the Neighbor Output pseudo-Oracle, which outputs a process's
# declared left or right consequent neighbor
#================================================================================
# Methods
    #----------------------------------------------------------------------------
    # - Oracle Constructor
    #----------------------------------------------------------------------------
    def __init__(self):
        self.executions = 0

    #----------------------------------------------------------------------------
    # - Check Guard
    #----------------------------------------------------------------------------
    # * network : network to evaluate the oracles's action's guard against
    #----------------------------------------------------------------------------
    def guard(self, network):
        for pid in network.nodes:
            if network.nodes[pid].left != network.nodes[pid].declared_left:
                return True
            if network.nodes[pid].right != network.nodes[pid].declared_right:
                return True
            
        return False
    
    #----------------------------------------------------------------------------
    # - Execute Command
    #----------------------------------------------------------------------------
    # * network : network to execute the oracle's action on
    #----------------------------------------------------------------------------
    def command(self, network):
        for pid in network.nodes:
            if network.nodes[pid].left != network.nodes[pid].declared_left:
                network.nodes[pid].declared_left = network.nodes[pid].left
                break
            if network.nodes[pid].right != network.nodes[pid].declared_right:
                network.nodes[pid].declared_right = network.nodes[pid].right
                break
        self.executions += 1

# Members
    name = "NO"
    executions = 0
#================================================================================

#================================================================================
class OracleCD:
#================================================================================
# Represents the Consequent Detector Oracle, which corrects any mistakenly
# declared neighbor to its true consequent neighbor
#================================================================================
# Methods
    #----------------------------------------------------------------------------
    # - Oracle Constructor
    #----------------------------------------------------------------------------
    def __init__(self):
        self.executions = 0

    #----------------------------------------------------------------------------
    # - Check Guard
    #----------------------------------------------------------------------------
    # * network : network to evaluate the oracles's action's guard against
    #----------------------------------------------------------------------------
    def guard(self, network):
        for pid in network.nodes:
            if network.nodes[pid].left != network.nodes[pid].declared_left and network.nodes[pid].left is network.linearization[network.linearization.index(pid) - 1]:
                return True
            if network.nodes[pid].right != network.nodes[pid].declared_right and network.nodes[pid].right is network.linearization[network.linearization.index(pid) + 1]:
                return True
        return False
    
    #----------------------------------------------------------------------------
    # - Execute Command
    #----------------------------------------------------------------------------
    # * network : network to execute the oracle's action on
    #----------------------------------------------------------------------------
    def command(self, network):
        for pid in network.nodes:
            if network.nodes[pid].left != network.nodes[pid].declared_left and network.nodes[pid].left is network.linearization[network.linearization.index(pid) - 1]:
                network.nodes[pid].declared_left = network.nodes[pid].left
                break
            if network.nodes[pid].right != network.nodes[pid].declared_right and network.nodes[pid].right is network.linearization[network.linearization.index(pid) + 1]:
                network.nodes[pid].declared_right = network.nodes[pid].right
                break
        self.executions += 1

# Members
    name = "CD"
    executions = 0

#--------------------------------------------------------------------------------
# - List All Oracles
#--------------------------------------------------------------------------------
def get_oracles():
    return [OracleWC(), OraclePD(), OracleNO(), OracleCD()]