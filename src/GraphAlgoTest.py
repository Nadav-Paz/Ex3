import unittest
from DiGraph import DiGraph
from GraphAlgo import GraphAlgo


def graph_algo_a():
    g = DiGraph()
    for i in range(0,5):
        g.add_node(i)
    g.add_edge(0, 1, 5)
    g.add_edge(1, 0, 8)
    g.add_edge(0, 2, 2)
    g.add_edge(2, 0, 1)
    g.add_edge(2, 3, 1)
    g.add_edge(3, 2, 0.5)
    g.add_edge(3, 4, 12)
    g.add_edge(4, 3, 1)
    g.add_edge(0, 4, 20)
    g.add_edge(4, 0, 20)
    g.add_edge(4, 1, 5)
    g.add_edge(1, 4, 5)
    return g


class MyTestCase(unittest.TestCase):

    def test_dijkstra(self):
        g = GraphAlgo(graph_algo_a())
        g.dijkstra(0)
        self.assertEqual(10, g.get_graph().get_node(4).get_weight())


if __name__ == '__main__':
    unittest.main()
