import unittest

from main import *
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
        
        no_matches = extract_markdown_images("This is text with no images, wonder what it will return.")

        # print(no_matches)
        # print(matches)
        
    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com)")
        
        self.assertListEqual([("to boot dev", "https://www.boot.dev"),
                               ("to youtube", "https://www.youtube.com")], matches)
        
        no_matches = extract_markdown_links("This is text with no links, wonder what it will return.")


    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,)
        
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
        # print(new_nodes)

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual([
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
        ],
        new_nodes
        )


    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and " \
        "an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.assertListEqual([
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ], text_to_textnodes(text))

        text = "This is **bold**_italic_`code`"
        self.assertListEqual([
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode("italic", TextType.ITALIC),
            TextNode("code", TextType.CODE)
        ], text_to_textnodes(text))

        text = "Just plain text with nothing special."
        self.assertListEqual([
            TextNode("Just plain text with nothing special.", TextType.TEXT)
        ], text_to_textnodes(text))

        text = "**BoldStart** middle _italicEnd_"
        self.assertListEqual([
            TextNode("BoldStart", TextType.BOLD),
            TextNode(" middle ", TextType.TEXT),
            TextNode("italicEnd", TextType.ITALIC)
        ], text_to_textnodes(text))

        text = "Start ![img1](a.jpg) middle [site](http://x) end"
        self.assertListEqual([
            TextNode("Start ", TextType.TEXT),
            TextNode("img1", TextType.IMAGE, "a.jpg"),
            TextNode(" middle ", TextType.TEXT),
            TextNode("site", TextType.LINK, "http://x"),
            TextNode(" end", TextType.TEXT)
        ], text_to_textnodes(text))

        text = "here's an empty bold: **** and empty link: []()"
        self.assertListEqual([
            TextNode("here's an empty bold: ", TextType.TEXT),
            TextNode("", TextType.BOLD),
            TextNode(" and empty link: ", TextType.TEXT),
            TextNode("", TextType.LINK, "")
        ], text_to_textnodes(text))

        text = "![one](a.jpg)![two](b.png)[bootdev](https://boot.dev)"
        self.assertListEqual([
            TextNode("one", TextType.IMAGE, "a.jpg"),
            TextNode("two", TextType.IMAGE, "b.png"),
            TextNode("bootdev", TextType.LINK, "https://boot.dev")
        ], text_to_textnodes(text))


    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        
        blocks = markdown_to_blocks(md)

        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_blocktype_heading(self):
        md = "## Heading two"
        self.assertEqual(block_to_block_type(md), BlockType.HEADING)

        md = "#No space after hash"
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)

    def test_blocktype_code(self):
        md = "```\ncode\n```"
        self.assertEqual(block_to_block_type(md), BlockType.CODE)

        md = "```\ncode"
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)

    def test_blocktype_quote(self):
        md = "> a quote\n> another line"
        self.assertEqual(block_to_block_type(md), BlockType.QUOTE)

        md = ">partial\nnot quoted"
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)

    def test_blocktype_unordered(self):
        md = "- item one\n- item two"
        self.assertEqual(block_to_block_type(md), BlockType.UNORDERED_LIST)

        md = "item one\n* item two"
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)

    def test_blocktype_ordered(self):
        md = "1. one\n2. two\n3. three"
        self.assertEqual(block_to_block_type(md), BlockType.ORDERED_LIST)

        md = "1. one\n3. three"
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)

        md = "0. zero\n1. one"
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)

    def test_blocktype_paragraph(self):
        md = "Just plain text."
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)

        md = "Some text\n- but followed by a dash"
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)



    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading(self):
        md = "# Heading Example"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h1>Heading Example</h1></div>")

    def test_blockquote(self):
        md = "> This is a blockquote"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><blockquote>This is a blockquote</blockquote></div>")

    def test_unordered_list(self):
        md = "- item one\n- item two"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ul><li>item one</li><li>item two</li></ul></div>")

    def test_ordered_list(self):
        md = "1. first item\n2. second item"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ol><li>first item</li><li>second item</li></ol></div>")

    def test_paragraph(self):
        md = "Just a simple paragraph."
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><p>Just a simple paragraph.</p></div>")