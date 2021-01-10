from typing import List

import GraphInterface


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
                self._graph.add_node(node['id'], [float(x) for x in node['pos'].split(',')])
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
        path=[]
        for i in range(0,len(reversed_path)):
            path.append(reversed_path[len(reversed_path)-i-1])
        return self._graph.get_node(id2).get_weight(), path

    def connected_component(self, id1: int) -> list:
        pass

    def connected_components(self) -> List[list]:
        pass

    def tarjen_algo(self, node_id: int):

        for key, node in self._graph.get_all_v().values():
            node.set_info('white')
            node.set_tag(key)

        node = self._graph.get_node(node_id)



    def DFS(self,node_id: int):
        s = self._graph.get_node(node_id)
        s.set_info('black')
        st = []
        st.append(s)
        while not len(st) == 0:
            node = st[0]
            st.pop(0)
            for (n, w) in node.get_out_neighbors().values():
                neighbor = self._graph.get_node(n)
                if neighbor.get_info() == 'white':
                    neighbor.set_info('grey')
                    st.append(neighbor)



    def plot_graph(self) -> None:
        plt.figure()
        geox=[]
        geoy=[]
        i=0
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

