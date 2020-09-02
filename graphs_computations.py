import set_operations
import matplotlib.pyplot as plt
import math
from typing import List
import networkx
from itertools import count
import colors

class VictoryGraph(dict):

    @staticmethod
    def orgenise_hierarchy(hierarchy):
        invert_str = lambda target:"".join(["1" if ch == "0" else "0" for ch in target])
        ret:list = [None]*len(hierarchy)
        hierarchy = set(hierarchy)
        for current_index_to_fill in range(len(ret)//2):
            max_target = max(hierarchy)
            ret[current_index_to_fill] = max_target
            ret[current_index_to_fill + len(ret)//2] = invert_str(max_target)
            hierarchy -= set(ret)
        return ret

    def plot(self,hierarchies:List[set]=None,hierarchy_values:List[float]=None):
        networkx_graph = self.to_networkx_graph()

        if hierarchies is not None:
            colors_iter = colors.make_iter()
            hierarchies = [self.orgenise_hierarchy(h) for h in hierarchies]
            pos = networkx.shell_layout(networkx_graph, nlist=hierarchies, rotate=math.pi/3)
            for hei,val in zip(hierarchies,hierarchy_values):
                radius = (pos[hei[0]][0]**2 + pos[hei[0]][1]**2)**0.5
                ring = plt.Circle((0,0),radius,fill=False,label="{:.2f}".format(val),linestyle="--",alpha=0.3,color=next(colors_iter))
                plt.gca().add_patch(ring)
            plt.legend()
        else:
            pos = networkx.kamada_kawai_layout(networkx_graph)

        networkx.draw(networkx_graph,with_labels =True,pos=pos,node_size=600,node_color=(0.7,0.3,0.4),arrowsize=14,font_size=10,edge_color=(0,0,0,0.35))
        plt.axis("equal")

    def print(self):
        targets = self.keys()
        for p1 in targets:
            print("{} : {}".format(p1," ".join(self[p1])))

    def get_loops(self):
        networkx_graph = self.to_networkx_graph()
        return networkx.simple_cycles(networkx_graph)

    def get_number_of_loops(self):
        loops_gen = self.get_loops()
        n = 0
        for l in loops_gen:
            n += 1
            if n % 100000 == 0:
                print(n)

        return n


    def to_networkx_graph(self):
        edges = [couple for couple in set_operations.get_all_couples(self.keys())
                 if couple[0] in self[couple[1]]]
        return networkx.DiGraph(edges)
