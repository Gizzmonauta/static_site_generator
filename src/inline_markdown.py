from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    validate_split_nodes_delimiter_args(old_nodes, delimiter, text_type)
    if not old_nodes:
        return []
    new_nodes = []
    for node in old_nodes:
        if not node:
            continue
        if delimiter not in node.text or node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        parts = node.text.split(delimiter)
        part_index = 0
        while part_index < len(parts):
            if parts[part_index] == "":
                part_index += 1
                continue
            if part_index % 2 == 0:
                new_nodes.append(TextNode(parts[part_index], TextType.TEXT))
            else:
                new_nodes.append(TextNode(parts[part_index], text_type))
            part_index += 1
    return new_nodes

def validate_split_nodes_delimiter_args(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> None:
    if not isinstance(old_nodes, list):
        raise ValueError("old_nodes must be a list")
    if not isinstance(delimiter, str) or delimiter == "":
        raise ValueError("Delimiter must be a non-empty string")
    if not isinstance(text_type, TextType):
        raise ValueError("text_type must be a valid TextType")
    for node in old_nodes:
        if not isinstance(node, TextNode):
            raise ValueError("All elements in old_nodes must be TextNode instances")
        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise ValueError("Invalid Markdown syntax: unmatched delimiter")
        
def main():
    nodes = [TextNode("This is **bold** text", TextType.TEXT)]
    delimiter = "**"
    text_type = TextType.BOLD
    new_nodes = split_nodes_delimiter(nodes, delimiter, text_type)
    print(new_nodes,"\n\n")

    node = TextNode("This is text with a `code block` word", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    print(new_nodes,"\n\n")

    node = [
            TextNode("This has `code`", TextType.TEXT),
            TextNode("already bold", TextType.BOLD),
            TextNode("This also has `code` in it", TextType.TEXT)
        ]
    new_nodes = split_nodes_delimiter(node, "`", TextType.CODE)
    print(new_nodes,"\n\n")

    node = TextNode("code `code` code", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    print(new_nodes,"\n\n")
if __name__ == "__main__":
    main()