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
        return False
    
    #----------------------------------------------------------------------------
    # - Execute Command
    #----------------------------------------------------------------------------
    # * network : network to execute the oracle's action on
    #----------------------------------------------------------------------------
    def command(self, network):
        self.executions += 1

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