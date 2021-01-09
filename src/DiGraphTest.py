import unittest
from DiGraph import DiGraph
from src.DiGraph import DiGraph


class MyTestCase(unittest.TestCase):

    def GraphBilder(self, n: int):
        G: DiGraph = DiGraph()  # type : DiGraph
        for i in range(0, n):
            G.add_node(i, (i, i))
        for i in range(0, n):
            for j in range(0, n):
                if not i == j:
                    G.add_edge(i, j, 1)
                    G.add_edge(j, i, 1)
        return G
    def testEdgeSize(self):
        g=self.GraphBilder(5)
        self.assertEqual(20, g.e_size())
    def testNode1(self):
        g = self.GraphBilder(5)
        self.assertNotEqual(None, g.get_node(0))
    def testNode2(self):
        g = self.GraphBilder(5)
        self.assertEqual(None, g.get_node(7))

    def testAllIn(self):
        g = self.GraphBilder(5)
        D = g.all_in_edges_of_node(0)
        self.assertEqual(4, len(D))

    def testAllOut(self):
        g = self.GraphBilder(5)
        D = g.all_out_edges_of_node(0)
        self.assertEqual(4, len(D))

    def testCompereNode(self):
        g = self.GraphBilder(5)
        N1 = g.get_node(0)
        N1.set_weight(3)
        N2 = g.get_node(1)
        N2.set_weight(2)
        self.assertTrue(N1 > N2)



if __name__ == '__main__':
    #runner = unittest.TextTestRunner()
    #runner.run(test_main())
    unittest.main()
