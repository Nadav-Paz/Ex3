from typing import List

import GraphInterface
import matplotlib.pyplot as plt
import numpy as np
import math
import heapq

from GraphAlgoInterface import GraphAlgoInterface
from DiGraph import DiGraph


class GraphAlgo(GraphAlgoInterface):

    def __init__(self, graph):
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

        queue = [self._graph.get_node(s)]
        queue[0].set_weight(0.0)

        while queue:
            node = heapq.heappop(queue)
            node.set_info('black')

            for (n, w) in node.get_out_neighbors().values():
                print(node.get_key(), node.get_out_neighbors())
                neighbor = self._graph.get_node(n)
                if neighbor.get_info() == 'white':
                    neighbor.set_info('grey')
                    heapq.heappush(queue, neighbor)

                if neighbor.get_weight() > node.get_weight() + w:
                    neighbor.set_weight(node.get_weight() + w)
                    neighbor.set_tag(node.get_key())

    def load_from_json(self, file_name: str) -> bool:
        pass

    def save_to_json(self, file_name: str) -> bool:
        pass

    def shortest_path(self, id1: int, id2: int) -> (float, list):

        if self._graph.get_node(id1) is None or self._graph.get_node(id2) is None:
            return -1, []
        if self._graph.get_node(id1) == self._graph.get_node(id2):
            return 0, [self._graph.get_node(id1)]

        reversed_path = []
        self.dijkstra(id1)
        print('ron == roman')
        node = self._graph.get_node(id2)

        while node.get_tag() != -1:
            print(node.get_tag(), end=', ')
            reversed_path.append(node)
            node = self._graph.get_node(node.get_tag())
        path = [reversed_path[x-1] for x in range(len(reversed_path), 0, -1)]
        return self._graph.get_node(id2).get_weight(), path

    def connected_component(self, id1: int) -> list:
        pass

    def connected_components(self) -> List[list]:
        pass

    def plot_graph(self) -> None:
        pass

    def get_graph(self) -> GraphInterface:
        return self._graph

