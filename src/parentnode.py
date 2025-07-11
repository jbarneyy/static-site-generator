from htmlnode import HTMLNode

class ParentNode(HTMLNode):

    def __init__(self, tag: str, children: list[HTMLNode], props: dict | None = None):
        super().__init__(tag, None, children, props)
        
    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode requires a tag")
        
        if self.children is None or len(self.children) == 0:
            raise ValueError("ParentNode requires children")
        
        start_tag = f"<{self.tag}>"
        end_tag = f"</{self.tag}>"

        if self.tag == "a" and self.props is not None:
            start_tag = f"<{self.tag}{self.props_to_html()}>"

        if self.tag == "img" and self.props is not None:
            start_tag = f"<{self.tag}{self.props_to_html()} />"
            end_tag = ""

        inner_tag = ""
        for child_node in self.children:
            inner_tag += child_node.to_html()

        return start_tag + inner_tag + end_tag

        
        
