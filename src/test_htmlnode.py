import unittest

from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode


class Test(unittest.TestCase):

    def setUp(self):
        self.HTMLnode1 = HTMLNode()
        self.HTMLnode2 = HTMLNode()
        self.HTMLnode3 = HTMLNode("p", "This is a paragraph", None, {"href": "https://www.google.com"})

        self.leaf_node_1 = LeafNode("p", "This is a basic paragraph.")
        self.leaf_node_2 = LeafNode("p", "Hello, world!")
        self.leaf_node_3 = LeafNode("a", "Click Me!", {"href": "https://www.google.com"})

    def test_eq(self):
        self.assertEqual(self.HTMLnode1, self.HTMLnode2)
        self.assertEqual(self.leaf_node_2.to_html(), "<p>Hello, world!</p>")
        self.assertEqual(self.leaf_node_3.to_html(), '<a href="https://www.google.com">Click Me!</a>')

    def test_props_to_html(self):
        self.assertEqual(self.HTMLnode3.props_to_html(), ' href="https://www.google.com"')

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])

        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])

        self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild</b></span></div>")

    def test_to_html_with_nested_parents(self):
        grandparent_node = ParentNode("div", [ParentNode("span", [LeafNode("b", "world")])])

        self.assertEqual(grandparent_node.to_html(), "<div><span><b>world</b></span></div>")

    def test_to_html_with_no_children(self):
        parent_node = ParentNode("div", [])

        self.assertRaises(ValueError, parent_node.to_html)