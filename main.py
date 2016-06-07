from network import Network
from process import Process
import random
import action

net = Network(5, 1, 20)
for node_id in net.nodes:
    print net.nodes[node_id]

print "linear:", net.linearization

chosen = random.choice(net.nodes.keys())
print "p"+str(net.nodes[chosen]), "executed", net.nodes[chosen].act()
print chosen
net.nodes[chosen].send(chosen, "sa :J")
print net.nodes[chosen].channel
print action.ACTIONS[1].guard(net.nodes[chosen])
print net.linearized()
