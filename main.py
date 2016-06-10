from network import Network
from process import Process
from simulation import Simulator
import oracle
import random
import action

sim = Simulator()
sim.run_fault_experiment([40])