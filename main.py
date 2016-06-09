from network import Network
from process import Process
from simulation import Simulator
import oracle
import random
import action

sim = Simulator()
states = sim.run_fault_experiment([0, 100])
sim.record_results()