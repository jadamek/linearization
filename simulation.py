from network import Network
import random, numpy, sys
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
        #log = open("logs/trace.txt", 'w')
        state = 0

        channel_lengths = 0.0

        network = Network(population, 1, 1000)
        network.perturb(faults)        
        oracles = get_oracles()

        # Print block
        """        
        log.write("Initial state:\n")
        log.write("--Network--\n")
        for process in network.nodes:
            channel = "["
            for message in network.nodes[process].channel:
                channel += str(message) + " "
            channel += "]"
            log.write(str(network.nodes[process]))
            log.write("\tch:")
            log.write(str(channel))
            log.write("\n")
        log.write("-----------\n")
        
        
        print "Initial state:"
        print "--Network--"
        for process in network.nodes:
            channel = "["
            for message in network.nodes[process].channel:
                channel += str(message) + " "
            channel += "]"
            print network.nodes[process], "\tch:", channel
        print "-----------"
        """
        while not network.linearized():
            channel_lengths += numpy.mean([len(network.nodes[id].channel) for id in network.nodes])
            state += 1

            enabled = [network.nodes[id] for id in network.nodes if network.nodes[id].enabled()]

            # Select an action
            actions = [oracle for oracle in oracles if oracle.guard(network)]
            if len(enabled) > 0: actions += ["node"]
            chosen_action = random.choice(actions)
            
            #for oracle in oracles:
            #    log.write(oracle.name + ": " + str(oracle.guard(network)) + " ")
            #log.write("\n")
            
            if chosen_action == "node":
                actor = random.choice(enabled)
                action = actor.act()
                #log.write("s")
                #log.write(str(state))
                #log.write(": p")
                #log.write(str(actor.id))
                #log.write(" executes ")
                #log.write(str(action))
                #log.write("\n")
            else:
                chosen_action.command(network)
                #log.write("s")
                #log.write(str(state))
                #log.write(": ")
                #log.write(str(chosen_action.name))
                #log.write(" executes its action")
                #log.write("\n")
                #print "s"+str(state), ":", chosen_action.name, "executes its action"
                #print "s"+str(state), ":", chosen_action.name, "executes its action"

            # Print block
            """            
            log.write("--Network--\n")
            for process in network.nodes:
                channel = "["
                for message in network.nodes[process].channel:
                    channel += str(message) + " "
                channel += "]"
                log.write(str(network.nodes[process]))
                log.write("\tch:")
                log.write(str(channel))
                log.write("\n")
            log.write("-----------\n")
            
            print "--Network--"
            for process in network.nodes:
                channel = "["
                for message in network.nodes[process].channel:
                    channel += str(message) + " "
                channel += "]"
                print network.nodes[process], "\tch:", channel
            print "-----------"
            """
        return state, oracles[0].executions, oracles[3].executions, oracles[1].executions, channel_lengths / max(state, 1)

    #----------------------------------------------------------------------------
    # - Run A Fault-Dependent Experiment
    #----------------------------------------------------------------------------
    # * fault_rates : discrete fault rates to vary (percent of network)
    # * population : number of total processes in the network
    #----------------------------------------------------------------------------
    def run_fault_experiment(self, fault_rates, computations = 1, population = 5):
        self.experiment = "fault"
        self.speed = {}
        self.wc_calls = {}
        self.cd_calls = {}
        self.pd_calls = {}
        self.channel_length = {}

        progress_log = open("logs/Linear-progress-" + self.experiment + "_" + str(fault_rates[0]) + "-" + str(fault_rates[len(fault_rates) - 1]) + ".txt", 'w')

        for rate in fault_rates:            
            self.speed[rate] = []
            self.wc_calls[rate] = []
            self.cd_calls[rate] = []
            self.pd_calls[rate] = []
            self.channel_length[rate] = []

            for comp in range(computations):
                speed, wc_calls, cd_calls, pd_calls, channel_length = self.compute(int(population * rate / 100), population)
                self.speed[rate].append(speed)
                self.wc_calls[rate].append(wc_calls)
                self.cd_calls[rate].append(cd_calls)
                self.pd_calls[rate].append(pd_calls)
                self.channel_length[rate].append(channel_length)

                if computations >= 10:
                    if comp % (computations / 10) == 0:
                        progress_log.write(str(rate)+ " :  " + str(comp * 100 / computations) + "% Complete ... (" + str(comp) + "/" + str(computations) + ")\n")
                        progress_log.flush()

    #----------------------------------------------------------------------------
    # - Output Results
    #----------------------------------------------------------------------------
    # * filename : name of file to write experimental results to
    # * abcissa : the independent variable range as an array of values
    #----------------------------------------------------------------------------
    def record_results(self, filename, abscissa):
        results = open("logs/" + filename, 'w')

        results.write("-" * 80 + "\n")
        results.write("--\t\t\tExperimental results varying " + self.experiment + "\t\t      --\n")
        results.write("-" * 80 + "\n")
        results.write(self.experiment + "\tSpeed\t\tCD Calls\tWC Calls\tPD Calls\tChannel Length\n")
        results.write("\tMean\tSt.Dev" * 5 + "\n")
        results.write("-" * 80 + "\n")

        for x in abscissa:
            results.write(str(x))
            results.write("\t" + str(numpy.mean(self.speed[x])) + "\t" + str(numpy.std(self.speed[x])))
            results.write("\t" + str(numpy.mean(self.cd_calls[x])) + "\t" + str(numpy.std(self.cd_calls[x])))
            results.write("\t" + str(numpy.mean(self.wc_calls[x])) + "\t" + str(numpy.std(self.wc_calls[x])))
            results.write("\t" + str(numpy.mean(self.pd_calls[x])) + "\t" + str(numpy.std(self.pd_calls[x])))
            results.write("\t" + str(numpy.mean(self.channel_length[x])) + "\t" + str(numpy.std(self.channel_length[x])))
            results.write("\n")

# Members
    wc_calls = {}
    cd_calls = {}
    pd_calls = {}
    speed = {}
    channel_length = {}
    experiment = ""
#================================================================================
