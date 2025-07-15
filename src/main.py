from textnode import TextNode, TextType
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode

from enum import Enum
import re


def main():
    dummy_node = TextNode("This is anchor text", TextType.LINK, "https://www.boot.dev")
    second_node = TextNode("Any text", TextType.TEXT, "https://www.boot.dev")



main()