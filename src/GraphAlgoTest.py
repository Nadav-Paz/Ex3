import unittest
from DiGraph import DiGraph
from GraphAlgo import GraphAlgo
from src.Point import Point
import math


def graph_algo_a():
    g = DiGraph()
    for i in range(0, 5):
        geo=Point(i,100*math.sin(math.radians(i)+i-i*i))
        g.add_node(i)
        g.get_node(i).set_point(geo)
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

def graph_algo_b():
    g = DiGraph()
    for i in range(0, 8):
        g.add_node(i)
    g.get_node(0).set_point(Point(30,10))
    g.get_node(1).set_point(Point(40, 10))
    g.get_node(2).set_point(Point(40, 100))
    g.get_node(3).set_point(Point(10, 100))
    g.get_node(4).set_point(Point(20, 100))
    g.get_node(5).set_point(Point(20, 10))
    g.get_node(6).set_point(Point(30, 100))
    g.get_node(7).set_point(Point(10, 10))
    g.add_edge(0, 1, 1)
    g.add_edge(1, 2, 2)
    g.add_edge(2, 0, 1)
    g.add_edge(5,0,1)
    g.add_edge(5, 6, 1)
    g.add_edge(6, 0, 1)
    g.add_edge(6, 4, 1)
    g.add_edge(6, 2, 0.7)
    g.add_edge(4,5,0.2)
    g.add_edge(3,7,3)
    g.add_edge(7,3,7)
    g.add_edge(3,4,0.1)
    g.add_edge(7,5,1.5)
    a=GraphAlgo(g)
    a.plot_graph()
    return g

class MyTestCase(unittest.TestCase):

    def test_dijkstra1(self):
        g = GraphAlgo(graph_algo_a())
        g.dijkstra(0)
        self.assertEqual(10, g.get_graph().get_node(4).get_weight())

    def test_shortest_path1(self):
        g = GraphAlgo(graph_algo_a())
        self.assertEqual(3, len(g.shortest_path(0, 4)[1]))

    def test_dijkstra2(self):
        g = GraphAlgo(graph_algo_a())
        g.dijkstra(4)
        self.assertEqual(2.5, g.get_graph().get_node(0).get_weight())

    def test_shortest_path2(self):
        g = GraphAlgo(graph_algo_a())
        g.plot_graph()
        self.assertEqual(4, len(g.shortest_path(4, 0)[1]))

    def test_remove(self):
        g = GraphAlgo(graph_algo_a())
        g.get_graph().remove_node(2)
        self.assertEqual(13, g.shortest_path(4, 0)[0])

    def test_connected_component(self):
        g = GraphAlgo(graph_algo_a())
        print(g.connected_component(0))
        g.get_graph().printData()
        self.assertEqual(3,3)

    def test_connected_component2(self):
        g = GraphAlgo(graph_algo_b())
        print(g.connected_component(4))
        self.assertEqual(3,3)

    def test_json_write(self):
        g = GraphAlgo(graph_algo_a())
        self.assertTrue(g.save_to_json('D:\\json_test'))

    def test_json_just_read(self):
        g = GraphAlgo()
        self.assertTrue(g.load_from_json('D:\\json_test'))

    def test_json_read(self):
        g = GraphAlgo()
        g.load_from_json('D:\\json_test')
        self.assertTrue(GraphAlgo(graph_algo_a()).get_graph() == g.get_graph())

    def plot_test(self):
        g = GraphAlgo(graph_algo_a())
        g.plot_graph()


if __name__ == '__main__':
    unittest.main()

