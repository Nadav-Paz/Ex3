import unittest
from DiGraph import DiGraph
from GraphAlgo import GraphAlgo
from src.Point import Point
import math


def graph_algo_a():
    g = DiGraph()
    for i in range(0, 5):
        g.add_node(i)
    g.get_node(0).set_point(Point(10,100))
    g.get_node(1).set_point(Point(60, 100))
    g.get_node(2).set_point(Point(10, 50))
    g.get_node(3).set_point(Point(60, 50))
    g.get_node(4).set_point(Point(35, 10))
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
    # a = GraphAlgo(g)
    # a.plot_graph()
    return g

def concteted_graph_builder(n: int):
    g = DiGraph()
    k=-1
    for i in range(0, n):
        j=i%5
        if j==0:
            k+=1
        p=Point(10*(1+j),100*k)
        g.add_node(i)
        g.get_node(i).set_point(p)
    g.add_edge(0,1,1)
    g.add_edge(1,0,0.2)
    for i in range(2,n):
        g.add_edge(1,i,1)
        g.add_edge(i,1,0.5)

    #a = GraphAlgo(g)
    #a.plot_graph()
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
        self.assertEqual(4, len(g.shortest_path(4, 0)[1]))

    def test_remove(self):
        g = GraphAlgo(graph_algo_a())
        g.get_graph().remove_node(2)
        self.assertEqual(13, g.shortest_path(4, 0)[0])

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

    def test_connected_components(self):
        g = GraphAlgo(graph_algo_a())
        scc = g.connected_components()
        self.assertTrue(1 == len(scc) and g.get_graph().v_size() == len(scc[0]))

    def test_connected_components2(self):
        g = GraphAlgo(concteted_graph_builder(10))
        scc = g.connected_components()
        self.assertTrue(1 == len(scc))

    def test_connected_components3(self):
        g = GraphAlgo(concteted_graph_builder(1000))
        scc = g.connected_components()
        self.assertTrue(1 == len(scc))

    ''' def test_connected_components4(self):
        g = GraphAlgo(concteted_graph_builder(1000000))
        scc = g.connected_components()
        self.assertTrue(1 == len(scc))'''

    def test_connected_component(self):
        g = GraphAlgo(graph_algo_b())
        self.assertEqual(3, len(g.connected_component(0)))

    def test_plot(self):
        g = GraphAlgo(graph_algo_b())
        g.plot_graph()
        g = GraphAlgo(graph_algo_a())
        g.plot_graph()
        g = GraphAlgo(concteted_graph_builder(10))
        g.plot_graph()
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()

