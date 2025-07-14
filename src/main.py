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
            return_nodes.append(node)
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
                    
            # Catches empty delimiter nodes that are not TextType.TEXT #
            else:
                if i % 2 != 0:
                    new_nodes.append(TextNode(string, text_type))
        
        return_nodes.extend(new_nodes)
    
    return return_nodes

def split_nodes_image(old_nodes: list[TextNode]):
    return_nodes = []

    for node in old_nodes:
        new_nodes = []

        if node.text_type is not TextType.TEXT:
            return_nodes.append(node)
            continue

        markdown_images = extract_markdown_images(node.text)

        if not markdown_images:
            return_nodes.append(node)
            continue

        while markdown_images:
            pair = markdown_images[0]

            sections = node.text.split(f"![{pair[0]}]({pair[1]})", 1)

            pre_text = sections[0]
            post_text = sections[1]

            if pre_text:
                new_nodes.append(TextNode(pre_text, TextType.TEXT))
            
            new_nodes.append(TextNode(pair[0], TextType.IMAGE, pair[1]))

            node.text = post_text
            markdown_images = extract_markdown_images(node.text)

        if node.text:
            new_nodes.append(TextNode(node.text, TextType.TEXT))
        
        return_nodes.extend(new_nodes)

    return return_nodes

def split_nodes_link(old_nodes: list[TextNode]):
    return_nodes = []

    for node in old_nodes:
        new_nodes = []

        if node.text_type is not TextType.TEXT:
            return_nodes.append(node)
            continue

        markdown_images = extract_markdown_links(node.text)

        if not markdown_images:
            return_nodes.append(node)
            continue

        while markdown_images:
            pair = markdown_images[0]

            sections = node.text.split(f"[{pair[0]}]({pair[1]})", 1)

            pre_text = sections[0]
            post_text = sections[1]

            if pre_text:
                new_nodes.append(TextNode(pre_text, TextType.TEXT))
            
            new_nodes.append(TextNode(pair[0], TextType.LINK, pair[1]))

            node.text = post_text
            markdown_images = extract_markdown_links(node.text)

        if node.text:
            new_nodes.append(TextNode(node.text, TextType.TEXT))
        
        return_nodes.extend(new_nodes)

    return return_nodes

def text_to_textnodes(text: str):
    nodes = [TextNode(text, TextType.TEXT)]

    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)

    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)

    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    nodes = split_nodes_image(nodes)

    nodes = split_nodes_link(nodes)

    return nodes


def extract_markdown_images(text: str):
    string_matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

    return string_matches

def extract_markdown_links(text: str):
    string_matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

    return string_matches






main()