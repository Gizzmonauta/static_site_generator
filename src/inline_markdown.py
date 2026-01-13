from textnode import TextNode, TextType
import re

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
        
def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text) -> list[tuple[str, str]]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    """
    Split TextType.TEXT nodes containing markdown links into multiple nodes:
    plain text nodes and TextType.LINK nodes with URLs.
    """
    validate_split_nodes_images_and_links_args(old_nodes)
    if not old_nodes:
        return []
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        images: list[tuple[str, str]] = extract_markdown_images(node.text)
        if not images:
            new_nodes.append(node)
            continue
        remaining_text: str = node.text
        for image_text, image_url in images:
            md_snippet: str = f"![{image_text}]({image_url})"
            before, after = remaining_text.split(md_snippet, 1)
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(image_text, TextType.IMAGE, image_url))
            remaining_text = after
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    """
    Split TextType.TEXT nodes containing markdown links into multiple nodes:
    plain text nodes and TextType.LINK nodes with URLs.
    """
    validate_split_nodes_images_and_links_args(old_nodes)
    if not old_nodes:
        return []
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        links: list[tuple[str, str]] = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
            continue
        remaining_text: str = node.text
        for link_text, link_url in links:
            md_snippet: str = f"[{link_text}]({link_url})"
            before, after = remaining_text.split(md_snippet, 1)
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
            remaining_text = after
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes

def validate_split_nodes_images_and_links_args(old_nodes: list[TextNode]) -> None:
    if not isinstance(old_nodes, list):
        raise ValueError("old_nodes must be a list")
    for node in old_nodes:
        if not isinstance(node, TextNode):
            raise ValueError("All elements in old_nodes must be TextNode instances")

        
def main():
    node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
    )
    new_nodes = split_nodes_image([node])
    print(new_nodes, "\n\n")
    #     [
    #         TextNode("This is text with an ", TextType.TEXT),
    #         TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
    #         TextNode(" and another ", TextType.TEXT),
    #         TextNode(
    #             "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
    #         ),
    #     ],
 
    node = TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT,
    )
    new_nodes = split_nodes_link([node])
    print(new_nodes, "\n\n")
    #     [
    #         TextNode("This is text with a link ", TextType.TEXT),
    #         TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
    #         TextNode(" and ", TextType.TEXT),
    #         TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
    #     ],

    nodes = [
        TextNode("This has `code`", TextType.TEXT),
        TextNode("already bold", TextType.BOLD),
        TextNode("This also has `code` in it", TextType.TEXT),
        TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT),
        TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT),
        TextNode('[John](https://www.john.com)![Mary](https://www.mary.com)![Jerry](https://www.jerry.com)', TextType.TEXT)
    ]
    new_nodes = split_nodes_image(nodes)
    print(new_nodes, "\n\n")

if __name__ == "__main__":
    main()