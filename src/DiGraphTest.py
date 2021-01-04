import unittest
from DiGraph import DiGraph

class MyTestCase(unittest.TestCase):

    def GraphBilder(self, n: int):
        G: DiGraph = DiGraph()
        G.__init__()
        for i in range(0, n):
             G.add_node(i, (i, i))
        for i in range(0, n):
            for j in range(0, n):
                if not i == j:
                    G.add_edge(i, j, 1)
                    G.add_edge(j, i, 1)
        return G

    def test_something(self):
        G: DiGraph = self.GraphBilder(5)
        self.assertEqual(G.e_size(), 20)
        self.assertEqual(True, True)

if __name__ == '__main__':
    unittest.main()
