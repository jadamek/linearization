from network import Network
from process import Process
from simulation import Simulator
from numpy import inf
import oracle
import random
import action

sim = Simulator()
sim.run_fault_experiment([40])
sim.record_results()
