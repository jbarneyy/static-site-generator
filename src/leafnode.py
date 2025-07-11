from htmlnode import HTMLNode

class LeafNode(HTMLNode):

    def __init__(self, tag: str | None, value: str, props: dict | None = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode requires a value")
        
        if self.tag is None:
            return self.value
        
        start_tag = f"<{self.tag}>"
        end_tag = f"</{self.tag}>"
        
        if self.tag == "a" and self.props is not None:
            start_tag = f"<{self.tag}{self.props_to_html()}>"

        if self.tag == "img" and self.props is not None:
            start_tag = f"<{self.tag}{self.props_to_html()} />"
            end_tag = ""


        return start_tag + self.value + end_tag
    


