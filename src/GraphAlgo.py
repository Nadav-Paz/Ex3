from typing import List

import GraphInterface
import time

from GraphAlgoInterface import GraphAlgoInterface
from DiGraph import DiGraph
from Point import Point
from PriorityQueue import PriorityQueue
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
        self._mc = 0
        self._src_dijkstra = -1
        self.strongly_connected_components = []

    def dijkstra(self, s: int):
        if self._mc == self._graph.get_mc() and s == self._src_dijkstra:
            return
        GraphAlgo._mc = self._graph.get_mc()
        GraphAlgo._src_dijkstra = s

        for key, node in self._graph.get_all_v().values():
            node.set_info('white')
            node.set_tag(-1)
            node.set_weight(float('inf'))
        #self._graph.printData()
        queue = PriorityQueue();
        self._graph.get_node(s).set_weight(0.0)
        queue.insert(self._graph.get_node(s))

        while not queue.isEmpty():
            node=queue.delete()
            node.set_info('black')
            for (n, w) in node.get_out_neighbors().values():
                neighbor = self._graph.get_node(n)
                if neighbor.get_info() == 'white':
                    neighbor.set_info('grey')
                    queue.insert(neighbor)

                if neighbor.get_weight() > node.get_weight() + w:
                    neighbor.set_weight(node.get_weight() + w)
                    neighbor.set_tag(node.get_key())

        #self._graph.printData()

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

    def connected_component(self, id1: int) -> list:
        pass

    def connected_components(self) -> List[list]:
        pass

    def tarjan_algo(self, node_id: int):

        unique_key = str(time.time())
        tag = 0

        '''        
        for key, node in self._graph.get_all_v().values():
            node.set_info('white')
            node.set_tag(key)
        '''

        node = self._graph.get_node(node_id)
        node.set_info(unique_key)
        trajan_counter = 0

        trajan_stack = [node]
        dfs_stack = [node]
        low_link = {node.get_key(): trajan_counter}
        trajan_id = {node.get_key(): trajan_counter}
        on_stack = {node.get_key()}
        trajan_counter += 1

        for _key, node in self._graph.get_all_v().values():
            if node.get_info() != unique_key:
                node.set_info(unique_key)

                low_link[node.get_key()] = trajan_counter
                trajan_id[node.get_key()] = trajan_counter
                on_stack.add(node.get_key())

                trajan_counter += 1
                trajan_stack.append(node)
                dfs_stack.append(node)
                while dfs_stack:
                    node = dfs_stack.pop()
                    for key, weight in node.get_out_neighbors().values():
                        neighbor = self._graph.get_node(key)

                        if neighbor.get_info() != unique_key:
                            neighbor.set_info(unique_key)
                            neighbor.set_tag(tag)
                            tag += 1
                            trajan_stack.append(neighbor)
                            dfs_stack.append(neighbor)

                        elif neighbor.get_key() in trajan_stack:
                            neighbor.set_tag(min(node.get_tag(), neighbor.get_tag()))
                        else:
                            pass    # not interested

    def DFS(self, node_id: int, unique_key: str, tarjan_stack: list, low_link: dict, on_stack: set):
        s = self._graph.get_node(node_id)
        s.set_info(unique_key)
        dfs_stack = [s]
        while dfs_stack:
            node = dfs_stack.pop()
            for (key, weight) in node.get_out_neighbors().values():
                neighbor = self._graph.get_node(key)
                if neighbor.get_info() != unique_key:
                    neighbor.set_info(unique_key)
                    dfs_stack.append(neighbor)
                    tarjan_stack.append(neighbor)
                    #on_stack.add(neighbor.get_key())
                if neighbor.get_key() in on_stack:
                    low_link[neighbor.get_key()] = min(node.get_key(), neighbor.get_key())


    def plot_graph(self) -> None:
        plt.figure()
        geox = []
        geoy = []
        i = 0
        plt.grid()
        for key, node in self._graph.get_all_v().values():
            geox.append(node.get_point().get_x())
            geoy.append(node.get_point().get_y())
            for (n, w) in node.get_out_neighbors().values():
                neighbor = self._graph.get_node(n)
                ax=plt.axes()
                dx=neighbor.get_point().get_x()-node.get_point().get_x()
                dy = neighbor.get_point().get_y() - node.get_point().get_y()
                ax.arrow(node.get_point().get_x(),node.get_point().get_y(),dx,dy)
            i=i+1
        plt.scatter(geox,geoy,50)
        plt.xlabel(' X postion ')
        plt.ylabel(' y postion ')
        plt.title(' Graph ')
        plt.show();


    def get_graph(self) -> GraphInterface:
        return self._graph

