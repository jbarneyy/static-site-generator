from textnode import TextNode, TextType
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode

from enum import Enum
import re


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"



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


def markdown_to_blocks(markdown: str):
    block_list = markdown.split("\n\n")
    return [block.strip() for block in block_list if block]


def block_to_block_type(markdown_block: str):

    block_lines = markdown_block.split("\n")

    matched = re.match(r"#{1,6} ", block_lines[0])

    if matched:
        return BlockType.HEADING
    
    if markdown_block.startswith("```") and markdown_block.endswith("```"):
        return BlockType.CODE

    if all(line.startswith(">") for line in block_lines):
        return BlockType.QUOTE
    
    if all(line.startswith("- ") for line in block_lines):
        return BlockType.UNORDERED_LIST
    
    if all(line.startswith(f"{index}. ") for index, line in enumerate(block_lines, start=1)):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown: str):
    markdown_blocks = markdown_to_blocks(markdown)
    root_html_node = ParentNode("div", [])

    for block in markdown_blocks:
        block_type = block_to_block_type(block)
        html_node = None

        # Based on type of block, create new HTMLNode with proper data, should it be parent/leaf/html? #
        match block_type:
            case BlockType.PARAGRAPH:
                block = block.split("\n")
                block = " ".join(block)

                html_node = ParentNode("p", text_to_children(block))
            
            case BlockType.HEADING:
                matched = re.match(r"#{1,6} ", block.split("\n")[0])
                number_hashes = len(matched.group(0)) - 1

                html_node = ParentNode(f"h{number_hashes}", text_to_children(block[number_hashes+1:]))

            case BlockType.QUOTE:
                html_node = ParentNode("blockquote", text_to_children(block[2:]))

            case BlockType.UNORDERED_LIST:
                html_node = ParentNode("ul", [])
                for line in block.split("\n"):
                    html_node.children.append(ParentNode("li", text_to_children(line[2:])))
            
            case BlockType.ORDERED_LIST:
                html_node = ParentNode("ol", [])
                for line in block.split("\n"):
                    first_space_index = line.find(".")
                    html_node.children.append(ParentNode("li", text_to_children(line[first_space_index+2:])))

            case BlockType.CODE:
                trimmed_block = block.split("\n")
                trimmed_block = trimmed_block[1:len(trimmed_block)-1]
                trimmed_block = "\n".join(trimmed_block) + "\n"

                html_node = ParentNode("pre", [text_node_to_html_node(TextNode(trimmed_block, TextType.CODE))])

            case _:
                raise Exception("BlockType mismatch, no Block Type of this type.")
        
        root_html_node.children.append(html_node)
    
    return root_html_node


# Takes string of text and returns a list of HTMLNodes that represent the inline markdown using text_node_to_html_node #
def text_to_children(text: str):
    text_node_list = text_to_textnodes(text)
    return_list = []

    for text_node in text_node_list:
        return_list.append(text_node_to_html_node(text_node))

    return return_list



main()