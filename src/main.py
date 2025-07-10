from textnode import TextNode, TextType

def main():
    dummy_node = TextNode("This is anchor text", TextType.LINK, "https://www.boot.dev")
    second_node = TextNode("Any text", TextType.TEXT, "https://www.boot.dev")
    print(dummy_node)




main()