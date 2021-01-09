from GraphInterface import GraphInterface
from Point import Point


class DiGraph(GraphInterface):

    _nodeCounter = 0

    def __init__(self) -> object:
        self._vertices = dict()
        self._edges = dict()
        self._mc = 0

    def v_size(self) -> int:
        return len(self._vertices)

    def e_size(self) -> int:
        return len(self._edges)

    def get_mc(self) -> int:
        return self._mc

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        if self._vertices.__contains__(id1) and self._vertices.__contains__(id2):
            if not self._edges.__contains__((id1, id2)):

                self._mc += 1
                self._edges[(id1, id2)] = weight
                flag1= self._vertices[id1][1].add_out_neighbor(self.get_node(id2), weight)
                flag2= self._vertices[id2][1].add_in_neighbor(self.get_node(id1), weight)
                return flag1 and flag2

        return False

    def add_node(self, node_id: object, pos: object = None) -> object:
        """

        :rtype: object
        """
        if type(node_id) is not int:
            return False
        try:
            self._vertices[node_id] = (node_id, DiGraph.Node(key=node_id, point=Point(coordinate=pos)))
            self._mc += 1
            return True

        except KeyError:
            return False

    def remove_node(self, node_id: int) -> bool:
        if self._vertices.__contains__(node_id):
            return False

        for node, ___ in self.all_in_edges_of_node(node_id).values():
            self.remove_edge(node_id, node)
        for node, ___ in self.all_out_edges_of_node(node_id).values():
            self.remove_edge(node_id, node)
        self._vertices.pop(node_id)
        self._mc += 1

        return True

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        try:
            self._vertices[node_id1][1].remove_in_neighbor(node_id2)
            self._vertices[node_id2][1].remove_in_neighbor(node_id1)
            self._edges.pop((node_id1, node_id2))
            self._mc += 1
            return True

        except KeyError:
            return False

    def get_node(self, node_id: int):
        try:
            return self._vertices[node_id][1]
        except KeyError:
            return None

    def get_all_v(self) -> dict:
        return self._vertices

    def all_in_edges_of_node(self, id1: int) -> dict:
        try:
            return self._vertices[id1][1].get_in_neighbors()
        except KeyError as E:
            return dict()

    def all_out_edges_of_node(self, id1: int) -> dict:
        try:
            return self._vertices[id1][1].get_out_neighbors()
        except KeyError:
            return dict()

    class Node:

        def __init__(self, key=None, point=None, info='', tag=0, weight=0.0):

            DiGraph._nodeCounter += 1
            self._key = key if key else DiGraph._nodeCounter
            self._point = point.__copy__() if point else Point()
            self._info = info
            self._tag = tag
            self._weight = weight
            self._in_neighbors = dict()
            self._out_neighbors = dict()

        def get_key(self):
            return self._key

        def get_info(self):
            return self._info

        def get_tag(self):
            return self._tag

        def get_point(self):
            return self._point

        def get_weight(self):
            return self._weight

        def set_info(self, info):
            self._info = info

        def set_tag(self, tag):
            self._tag = tag

        def set_weight(self, weight):
            self._weight = weight

        def set_point(self, point):
            self._point = point.__copy__()

        def add_in_neighbor(self, node, weight=0.0):
            if type(node) != DiGraph.Node:
                return False

            weight = weight if 0.0 < weight else 0.0
            self._in_neighbors.update({node.get_key(): (node.get_key(), weight)})
            return True

        def remove_in_neighbor(self, node):
            try:
                self._in_neighbors.pop(node)
                return True
            except KeyError:
                return False

        def get_in_neighbors(self):
            return self._in_neighbors

        def add_out_neighbor(self, node, weight=0.0):
            if type(node) != DiGraph.Node:
                return False

            weight = weight if 0.0 < weight else 0.0
            self._out_neighbors[node.get_key()] = (node.get_key(), weight)
            return True

        def remove_out_neighbor(self, node):
            try:
                self._out_neighbors.pop(node)
                return True
            except KeyError:
                return False

        def get_out_neighbors(self):
            return self._out_neighbors

        def __eq__(self, other):
            if type(other) is not DiGraph.Node:
                return False

            return other.get_key == self._key and self._point == other.get_point()

        def __gt__(self, other):
            return self.get_weight() > other.get_weight()

        def __ge__(self, other):
            return self.get_weight() >= other.get_weight()