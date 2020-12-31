from GraphInterface import GraphInterface
from Point import Point


class DiGraph(GraphInterface):

    _nodeCounter = 0

    def __init__(self):
        self._vertices = dict()
        self._edges = dict()

    def v_size(self) -> int:
        pass

    def e_size(self) -> int:
        pass

    def get_mc(self) -> int:
        pass

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        pass

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        pass

    def remove_node(self, node_id: int) -> bool:
        pass

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        pass

    class Node:

        def __init__(self, key=None, point=None, info='', tag=0, weight=0.0):

            DiGraph._nodeCounter += 1
            self._key = key if key else DiGraph._nodeCounter
            self._point = point.__copy__() if point else Point()
            self._info = info
            self._tag = tag
            self._weight = weight
            self._neighbors = dict()

        def get_key(self):
            return self._key

        def add_neighbor(self, node):
            if type(node) != DiGraph.Node:
                return False

            self._neighbors[node.get_key()] = node
            return True

    class Edge:

        def __init__(self):
            self._src = 0
            self._dst = 0
            self._weight = 0.0

