from htmlnode import HTMLNode

class LeafNode(HTMLNode):

    def __init__(self, value: str, tag: str | None, props: dict | None = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode requires a value.")
        
        if self.tag is None:
            return self.value
        
        start_tag = f"<{self.tag}>"
        end_tag = f"</{self.tag}>"

        if self.props is not None:
            start_tag = f"<{self.tag}{self.props_to_html()}>"

        return start_tag + self.value + end_tag
    


