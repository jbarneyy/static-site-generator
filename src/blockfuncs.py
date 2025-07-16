from enum import Enum
from parentnode import ParentNode
from textnode import TextNode, TextType
from textfuncs import text_node_to_html_node, text_to_textnodes

import re


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def extract_title(markdown: str):
    block_list = markdown_to_blocks(markdown)
    header_block = block_list[0]
    
    matched = re.match(r"#{1} ", header_block)

    if not matched:
        raise Exception("No h1 header")
    else:
        return header_block.strip("# ")


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
