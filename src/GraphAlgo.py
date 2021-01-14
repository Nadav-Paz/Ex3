from typing import List

import GraphInterface
import time

from GraphAlgoInterface import GraphAlgoInterface
from DiGraph import DiGraph
from Point import Point
#from PriorityQueue import PriorityQueue
from queue import PriorityQueue
import matplotlib.pyplot as plt
import json
from json import JSONEncoder
import math


class GraphEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, DiGraph):
            return {"Edges": [{"src": x[0], "w": o.get_edge(x[0], x[1]), "dest": x[1]} for x in o.get_all_e()],
                    "Nodes": [{"pos": str(o.get_node(y).get_point()), "id": y} for y in o.get_all_v()]}
        elif isinstance(o, DiGraph.Node):
            return {"pos": str(o.get_point()), "id": o.get_key()}
        else:
            return json.JSONEncoder.default(self, o)


class GraphAlgo(GraphAlgoInterface):

    def __init__(self, graph=None):
        self._graph = graph if graph else DiGraph()
        self._dijkstra_mc = 0
        self._tarjan_mc = 0
        self._src_dijkstra = -1
        self._strongly_connected_components_list_of_lists = []

    def shortest_path(self, id1: int, id2: int) -> (float, list):

        if self._graph.get_node(id1) is None or self._graph.get_node(id2) is None:
            return -1, []
        if self._graph.get_node(id1) == self._graph.get_node(id2):
            return 0, [self._graph.get_node(id1)]

        reversed_path = []
        self.dijkstra(id1)
        node = self._graph.get_node(id2)

        while node.get_tag() != -1:
            reversed_path.append(node)
            node = self._graph.get_node(node.get_tag())

        reversed_path.append(node)
        path = []
        for i in range(0, len(reversed_path)):
            path.append(reversed_path[len(reversed_path)-i-1])
        if len(path) == 1:
            if path[0].get_weight() == float('inf'):
                path = None
        return self._graph.get_node(id2).get_weight(), path

    def dijkstra(self, s: int):
        if self._dijkstra_mc == self._graph.get_mc() and s == self._src_dijkstra:
            return
        GraphAlgo._mc = self._graph.get_mc()
        GraphAlgo._src_dijkstra = s

        for node in self._graph.get_all_v().values():
            node.set_info('white')
            node.set_tag(-1)
            node.set_weight(float('inf'))

        queue = PriorityQueue()
        self._graph.get_node(s).set_weight(0.0)
        queue.put(self._graph.get_node(s))
        # queue.insert(self._graph.get_node(s))

        while not queue.empty():
            node = queue.get()
            # node = queue.delete()
            node.set_info('black')
            for n in node.get_out_neighbors():
                neighbor = self._graph.get_node(n)
                if neighbor.get_info() == 'white':
                    neighbor.set_info('grey')
                    queue.put(neighbor)

                if neighbor.get_weight() > node.get_weight() + node.get_out_neighbors()[n]:
                    neighbor.set_weight(node.get_weight() + node.get_out_neighbors()[n])
                    neighbor.set_tag(node.get_key())

    def load_from_json(self, file_name: str) -> bool:
        try:
            with open(file_name, 'r') as file:
                json_file = json.loads(file.read())
            self._graph = DiGraph()
            for node in json_file['Nodes']:
                if 'pos' in node.keys():
                    self._graph.add_node(node['id'], [float(x) for x in node['pos'].split(',')])
                else:
                    self._graph.add_node(node['id'])
            for edge in json_file['Edges']:
                self._graph.add_edge(edge['src'], edge['dest'], edge['w'])
            return True
        except:
            print("Error load_from_json")
            return False

    def save_to_json(self, file_name: str) -> bool:
        try:
            with open(file_name, 'w') as file:
                file.write(GraphEncoder().encode(self._graph))
                return True
        except:
            print("Error save_to_json")
            return False

    def connected_component(self, id1: int) -> list:
        if not self._graph.get_node(id1):
            return []

        if self._graph.get_mc() != self._tarjan_mc:
            return self.tarjan_algo(id1, True)

        for strongly_connected_component in self._strongly_connected_components_list_of_lists:
            if id1 in strongly_connected_component:
                return strongly_connected_component

    def connected_components(self) -> List[list]:
        if self._graph.get_mc() != self._tarjan_mc:
            for only_one_item in self._graph.get_all_v():
                self.tarjan_algo(only_one_item)
                break
            self._tarjan_mc = self._graph.get_mc()
        return self._strongly_connected_components_list_of_lists

    def tarjan_algo(self, node_id: int, return_value=False):
        self._strongly_connected_components_list_of_lists = []
        unvisited = set(self._graph.get_all_v().keys())
        low_link = {}
        trajan_id = {}
        on_stack = set()
        trajan_stack = []
        dfs_stack = []

        node = self._graph.get_node(node_id)
        unvisited.remove(node.get_key())

        while unvisited:
            if low_link:
                node = self._graph.get_node(unvisited.pop())
            dfs_stack.append(node)

            while dfs_stack:
                node = dfs_stack.pop()
                if node.get_key() not in on_stack:
                    dfs_stack.append(node)  # for callback
                    on_stack.add(node.get_key())
                    trajan_stack.append(node)
                    low_link[node.get_key()] = len(trajan_id)
                    trajan_id[node.get_key()] = len(trajan_id)

                    for key in node.get_out_neighbors().keys():
                        if key in unvisited:
                            unvisited.remove(key)
                            dfs_stack.append(self._graph.get_node(key))

                else:
                    for key in node.get_out_neighbors().keys():
                        if key in on_stack:
                            low_link[node.get_key()] = min(low_link[node.get_key()], low_link[key])

                    if trajan_id[node.get_key()] == low_link[node.get_key()] and node.get_key() in on_stack:
                        strongly_connected_component = []
                        while True:
                            flag = False
                            pop = trajan_stack.pop()
                            on_stack.remove(pop.get_key())
                            strongly_connected_component.append(pop.get_key())
                            if return_value:
                                if pop.get_key() == node_id:
                                    flag = True
                            if pop.get_key() == node.get_key():
                                strongly_connected_component.sort()
                                self._strongly_connected_components_list_of_lists.append(strongly_connected_component)
                                if flag:
                                    return strongly_connected_component
                                break

    def plot_graph(self) -> None:
        plt.figure()
        plt.grid()
        l = 5
        r = 500
        p = 0.33
        for key in self._graph.get_all_v():
            node = self._graph.get_node(key)
            ax = plt.axes()
            x = node.get_point().get_x()
            y = node.get_point().get_y()
            plt.scatter(x, y, r)
            for n in node.get_out_neighbors():
                neighbor = self._graph.get_node(n)
                dx = neighbor.get_point().get_x() - x
                dy = neighbor.get_point().get_y() - y
                if dy == 0:
                    ax.arrow(x, y, p * dx, p * dy, head_width=l, head_length=l / 5)
                else:
                    ax.arrow(x, y, p * dx, p * dy, head_width=l / 5, head_length=l)
                ax.arrow(x + p * dx, y + p * dy, (1 - p) * dx, (1 - p) * dy)
            ax.text(x, y, str(key), fontsize=10, color='white', weight="bold")
        plt.xlabel(' X postion ')
        plt.ylabel(' y postion ')
        plt.title(' Graph ')
        plt.show()

    def get_graph(self) -> GraphInterface:
        return self._graph

