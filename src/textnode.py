from enum import Enum

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    def __init__(self, text_content: str, text_type: str, url: str = None) -> None:
        self.text = text_content
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TextNode):
            return False
        if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
            return True
        return False
        
    def __repr__(self):
        return f"TextNode('{self.text}', '{self.text_type.value}', '{self.url}')"