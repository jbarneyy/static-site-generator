from __future__ import annotations

class HTMLNode():

    def __init__(self, tag: str | None = None, value: str | None = None, 
                 children: HTMLNode | None = None, props: dict | None = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplemented
    
    def props_to_html(self):
        ret = " "
        for pair in self.props.items():
            ret += f'{pair[0]}="{pair[1]}" '

        return ret.rstrip()
    
    def __repr__(self):
        return f"HTMLNode - Tag:{self.tag}, Value:{self.value}, Children:{self.children}, Props:{self.props}"
    
    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return False
        
        return (self.tag == other.tag and self.value == other.value and 
                self.children == other.children and self.props == other.props)
        
    
