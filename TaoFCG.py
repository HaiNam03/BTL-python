from androguard.misc import AnalyzeAPK
from androguard.core.analysis.analysis import ExternalMethod
import matplotlib.pyplot as plt
import networkx as nx

a, d, dx = AnalyzeAPK("apk_test.apk")

# Khao sat class
for d1 in dx.get_classes():
    print (d1)

CFG = nx.DiGraph()


for m in dx.find_methods(classname="Ljava/io/ObjectInputStream;"):
    orig_method = m.get_method()
    print("Found Method --> {}".format(orig_method))
    # orig_method might be a ExternalMethod too...
    # so you can check it here also:
    if isinstance(orig_method, ExternalMethod):
        is_this_external = True
        # If this class is external, there will be very likely
        # no xref_to stored! If there is, it is probably a bug in androguard...
    else:
        is_this_external = False

    CFG.add_node(orig_method, external=is_this_external)

    for other_class, callee, offset in m.get_xref_to():
        if isinstance(callee, ExternalMethod):
            is_external = True
        else:
            is_external = False

        if callee not in CFG.node:
            CFG.add_node(callee, external=is_external)

        # As this is a DiGraph and we are not interested in duplicate edges,
        # check if the edge is already in the edge set.
        # If you need all calls, you probably want to check out MultiDiGraph
        if not CFG.has_edge(orig_method, callee):
            CFG.add_edge(orig_method, callee)
plt.figure(figsize=(15, 8))
nx.draw_networkx(CFG, node_size=100, with_labels=True, font_size = 5, font_weight = "bold", arrowsize=20)
plt.draw()
plt.title("APK Function Call Graph")
plt.show()