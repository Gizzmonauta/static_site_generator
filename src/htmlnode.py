class HTMLNode():
    def __init__(self, tag: str = None, value: str = None, children: list = None, props: dict = None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        raise NotImplementedError("to_html method must be implemented by subclasses")
    
    def props_to_html(self) -> str:
        result = ""
        if self.props == None:
            return result
        for key, value in self.props.items():
            result += f' {key}="{value}"'
        return result
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, HTMLNode):
            return False
        if self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props:
            return True
        return False

    def __repr__(self) -> str:
        return f"HTMLNode(tag='{self.tag}', value='{self.value}', children={self.children}, props={self.props})"
    

class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: dict = None) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag is None:
            return f"{self.value}"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self) -> str:
        return f"LeafNode(tag='{self.tag}', value='{self.value}', props={self.props})"
    
    

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list, props: dict = None) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("All parent nodes must have a tag")
        if self.children is None:
            raise ValueError("All parent nodes must have children")
        the_inside: str = ""
        for child in self.children:
            if not isinstance(child, HTMLNode):
                raise ValueError("All children must be HTMLNode instances")
            the_inside += child.to_html()
            
        return f"<{self.tag}{self.props_to_html()}>{the_inside}</{self.tag}>"
    
    def __repr__(self) -> str:
        return f"ParentNode(tag='{self.tag}', children={self.children}, props={self.props})"
