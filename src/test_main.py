import unittest

from main import text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links
from textnode import TextNode, TextType
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode


class Test(unittest.TestCase):

    # Tests for text_node_to_html_node() #
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold text")

    def test_italic(self):
        node = TextNode("This is italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is italic text")

    def test_code(self):
        node = TextNode("This is code text", TextType.CODE)
        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is code text")

    def test_link(self):
        node = TextNode("Click Me!", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click Me!")
        self.assertEqual(html_node.props_to_html(), ' href="https://www.google.com"')

    def test_image(self):
        node = TextNode("This is alt text", TextType.IMAGE, "https://picsum.photos/200/300")
        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.to_html(), '<img src="https://picsum.photos/200/300" alt="This is alt text" />')


    # Tests for split_nodes_delimiter() #
    def test_delimiter_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(new_nodes[0], TextNode("This is text with a ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("code block", TextType.CODE))
        self.assertEqual(new_nodes[2], TextNode(" word", TextType.TEXT))

    def test_delimiter_bold(self):
        node = TextNode("foo **bar** baz **qux**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(new_nodes[0], TextNode("foo ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("bar", TextType.BOLD))
        self.assertEqual(new_nodes[2], TextNode(" baz ", TextType.TEXT))
        self.assertEqual(new_nodes[3], TextNode("qux", TextType.BOLD))

    def test_delimiter_italic(self):
        node1 = TextNode("Gimmie those _italics_", TextType.TEXT)
        node2 = TextNode("_italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node1, node2], "_", TextType.ITALIC)

        self.assertEqual(new_nodes[2], TextNode("italic", TextType.ITALIC))


    # Tests for extract_markdown_images() and extract_markdown_links() #
    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and" \
        "![rick roll](https://i.imgur.com/aKaOqIh.gif)")

        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"), 
                              ("rick roll", "https://i.imgur.com/aKaOqIh.gif")], matches)
        
    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com)")
        
        self.assertListEqual([("to boot dev", "https://www.boot.dev"),
                               ("to youtube", "https://www.youtube.com")], matches)
