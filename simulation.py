from network import Network
import random, numpy
from oracle import get_oracles

#================================================================================
class Simulator:
#================================================================================
# Implements experimental computations and full experiments, as well as result
# recording.
#================================================================================
# Methods
    #----------------------------------------------------------------------------
    # - Run Single Computation
    #----------------------------------------------------------------------------
    # * faults : number of processes to initially perturb (arbitrary state)
    # * population : number of total processes in the network
    #----------------------------------------------------------------------------
    def compute(self, faults, population):
        state = 0

        network = Network(population)
        network.perturb(faults)
        oracles = get_oracles()

        actions = [oracle for oracle in oracles if oracle.guard(network)] + ["node"]

        while not network.linearized() and state < 10:
            state += 1
            # Select an action
            action_type = random.choice(actions)

            if action_type is "node":
                actor = random.choice(network.nodes.keys())
                action = network.nodes[actor].act()
                print "s"+str(state), ": p"+str(actor), "executes", action
            else:
                action_type.command(network)
                print "s"+str(state), ":", action_type.name, "executes its action"

        return state, oracles[0].executions, oracles[3].executions

    #----------------------------------------------------------------------------
    # - Run A Fault-Dependent Experiment
    #----------------------------------------------------------------------------
    # * fault_rates : discrete fault rates to vary (percent of network)
    # * population : number of total processes in the network
    #----------------------------------------------------------------------------
    def run_fault_experiment(self, fault_rates, computations = 1, population = 5):
        self.experiment = "fault"
        self.speed = {}

        for rate in fault_rates:
            self.speed[rate] = []
            self.wc_calls[rate] = []
            self.cd_calls[rate] = []

            for comp in range(computations):
                speed, wc_calls, cd_calls = self.compute(int(population * rate), population)
                self.speed[rate].append(speed)
                self.wc_calls[rate].append(wc_calls)
                self.cd_calls[rate].append(cd_calls)

    #----------------------------------------------------------------------------
    # - Output Results
    #----------------------------------------------------------------------------
    # * filename : name of file to write experimental results to
    #----------------------------------------------------------------------------
    def record_results(self, filename = "ok"):
        print "--Experimental results varying", self.experiment, "--"
        print "stabilization speed:", self.speed
        print 'calls to WC Oracle:', self.wc_calls
        print "calls to CD Oracle:", self.cd_calls

# Members
    wc_calls = {}
    cd_calls = {}
    speed = {}
    experiment = ""
#================================================================================
