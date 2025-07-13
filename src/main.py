from textnode import TextNode, TextType
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
import re

def main():
    dummy_node = TextNode("This is anchor text", TextType.LINK, "https://www.boot.dev")
    second_node = TextNode("Any text", TextType.TEXT, "https://www.boot.dev")
    



def text_node_to_html_node(text_node: TextNode):

    text_type = text_node.text_type

    match text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        
        case _:
            raise Exception("TextNode is not one of the predefined types")
        

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType):
    return_nodes = []

    for node in old_nodes:
        new_nodes = []

        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue

        split_string_list = node.text.split(delimiter)
        if len(split_string_list) % 2 == 0:
            raise Exception(f"Delimiter mismatch in TextNode")
        
        for i in range(len(split_string_list)):
            string = split_string_list[i]

            if string:
                if i % 2 == 0:
                    new_nodes.append(TextNode(string, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(string, text_type))
        
        return_nodes.extend(new_nodes)
    
    return return_nodes


def extract_markdown_images(text: str):
    string_matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

    return string_matches

def extract_markdown_links(text: str):
    string_matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

    return string_matches











main()