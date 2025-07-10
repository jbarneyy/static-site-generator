from textnode import TextNode
from textnode import TextType

def main():
    dummy_node = TextNode("This is anchor text", TextType.LINK, "https://www.boot.dev")
    print(dummy_node)




main()