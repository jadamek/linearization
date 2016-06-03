from network import Network
from process import Process

net = Network(5, 1, 20)
for node_id in net.nodes:
    print net.nodes[node_id]