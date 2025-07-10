import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):

    def setUp(self):
        self.node1 = TextNode("This is a text node", TextType.BOLD)
        self.node2 = TextNode("This is a text node", TextType.BOLD)
        self.node3 = TextNode("This is a text node with URL", TextType.TEXT, "https://www.boot.dev")
        self.node4 = TextNode("This is a text node", TextType.TEXT)
        self.node5 = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")

    def test_eq(self):
        self.assertEqual(self.node1, self.node2)

    def test_instance(self):
        self.assertIsInstance(self.node3, TextNode)
        self.assertIsInstance(self.node2, TextNode)
        self.assertIsInstance(self.node1, TextNode)

    def test_not_eq(self):
        self.assertNotEqual(self.node1, self.node3)
        self.assertNotEqual(self.node1, self.node4)
        self.assertNotEqual(self.node5, self.node1)

    


if __name__ == "__main__":
    unittest.main()