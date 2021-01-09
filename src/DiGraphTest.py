import unittest
from DiGraph import DiGraph
from src.DiGraph import DiGraph


def graph_builder(n: int):
    g: DiGraph = DiGraph()  # type : DiGraph
    for i in range(0, n):
        g.add_node(i, (i, i))
    for i in range(0, n):
        for j in range(0, n):
            if not i == j:
                g.add_edge(i, j, 1)
                g.add_edge(j, i, 1)
    return g


class MyTestCase(unittest.TestCase):

    def testEdgeSize(self):
        g = graph_builder(5)
        self.assertEqual(20, g.e_size())

    def testNode1(self):
        g = graph_builder(5)
        self.assertNotEqual(None, g.get_node(0))

    def testNode2(self):
        g = graph_builder(5)
        self.assertEqual(None, g.get_node(7))

    def testAllIn(self):
        g = graph_builder(5)
        D = g.all_in_edges_of_node(0)
        self.assertEqual(4, len(D))

    def testAllOut(self):
        g = graph_builder(5)
        D = g.all_out_edges_of_node(0)
        self.assertEqual(4, len(D))

    def testCompereNode(self):
        g = graph_builder(5)
        n1 = g.get_node(0)
        n1.set_weight(3)
        n2 = g.get_node(1)
        n2.set_weight(2)
        self.assertTrue(n1 > n2)


if __name__ == '__main__':
    unittest.main()
