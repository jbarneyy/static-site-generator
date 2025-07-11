import unittest

from htmlnode import HTMLNode
from leafnode import LeafNode


class Test(unittest.TestCase):

    def setUp(self):
        self.HTMLnode1 = HTMLNode()
        self.HTMLnode2 = HTMLNode()
        self.HTMLnode3 = HTMLNode("p", "This is a paragraph", None, {"href": "https://www.google.com"})

        self.leaf_node_1 = LeafNode("This is a basic paragraph.", "p")
        self.leaf_node_2 = LeafNode("Hello, world!", "p")
        self.leaf_node_3 = LeafNode("Click Me!", "a", {"href": "https://www.google.com"})

    def test_eq(self):
        self.assertEqual(self.HTMLnode1, self.HTMLnode2)
        self.assertEqual(self.leaf_node_2.to_html(), "<p>Hello, world!</p>")
        self.assertEqual(self.leaf_node_3.to_html(), '<a href="https://www.google.com">Click Me!</a>')

    def test_props_to_html(self):
        self.assertEqual(self.HTMLnode3.props_to_html(), ' href="https://www.google.com"')

        

    