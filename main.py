from network import Network
from process import Process
from simulation import Simulator
from numpy import inf
import oracle
import random
import action
import time

start = time.clock()
sim = Simulator()
sim.run_fault_experiment(range(1, 11), 10, 10)
end = time.clock()
print "Experiment finished! (", end - start, "s)"
sim.record_results("Linear-results-faults_1-10.txt", range(1, 11))
