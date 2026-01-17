import os
from markdown_blocks import markdown_to_blocks, block_to_block_type
from blocknode import BlockType
from textnode import TextNode
from inline_markdown import text_to_textnodes
from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node


def markdown_to_html_node(markdown: str) -> HTMLNode:
    """
    Convert a markdown string to an HTML node representation.
    """
    blocks: list[str] = markdown_to_blocks(markdown)
    children: list[HTMLNode] = []
    for block in blocks:
        block_type: BlockType = block_to_block_type(block)
        node: HTMLNode = block_to_html_node(block, block_type)
        children.append(node)
    return ParentNode("div", children)

def block_to_html_node(block: str, block_type: BlockType) -> HTMLNode:
    """
    Convert a markdown block to an HTML node based on its BlockType.
    """
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    elif block_type == BlockType.CODE:
        return code_to_html_node(block)
    elif block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    elif block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    elif block_type == BlockType.UNORDERED_LIST:
        return unordered_list_to_html_node(block)
    elif block_type == BlockType.ORDERED_LIST:
        return ordered_list_to_html_node(block)
    else:
        raise ValueError(f"Unsupported BlockType: {block_type}")


def paragraph_to_html_node(block) -> HTMLNode:
    new_text: str = " ".join(block.split())
    html_children: list[HTMLNode] = text_to_children(new_text)
    return ParentNode("p", html_children)

def heading_to_html_node(block) -> HTMLNode:
    new_text: str = " ".join(block.split())
    prefix, text = new_text.split(" ", 1)
    level = min(len(prefix), 6)
    html_children: list[HTMLNode] = text_to_children(text)
    return ParentNode(f"h{level}", html_children)

def code_to_html_node(block) -> HTMLNode:
    code_content: list[str] = block.split("\n")
    inner_lines: list[str] = code_content[1:-1]  # remove fence lines

    # --- dedent by min indent across non-empty lines ---
    min_indent: int | None = None
    for line in inner_lines:
        if line.strip() == "":
            continue
        count = 0
        for ch in line:
            if ch == " ":
                count += 1
            else:
                break
        if min_indent is None or count < min_indent:
            min_indent = count
    if min_indent is None:
        min_indent = 0

    dedented_lines: list[str] = []
    for line in inner_lines:
        if line.strip() == "":
            dedented_lines.append("")
        else:
            dedented_lines.append(line[min_indent:])

    inner_content = "\n".join(dedented_lines)
    if not inner_content.endswith("\n"):
        inner_content += "\n"
    # --- end dedent ---

    leaf_node: LeafNode = LeafNode(None, inner_content)
    code_node: ParentNode = ParentNode("code", [leaf_node])
    return ParentNode("pre", [code_node])

def quote_to_html_node(block) -> HTMLNode:
    lines = block.split("\n")
    for i in range(len(lines)):
        lines[i] = lines[i].lstrip()[1:].lstrip()  # remove leading '> '
    quote_text = " ".join(lines)
    normalized_text = " ".join(quote_text.split())
    html_children: list[HTMLNode] = text_to_children(normalized_text)
    return ParentNode("blockquote", html_children)

def unordered_list_to_html_node(block) -> HTMLNode:
    lines = block.split("\n")
    li_nodes: list[HTMLNode] = []
    for line in lines:
        if line.strip() == "":
            continue
        item_text: str = line.lstrip()[1:].lstrip()  # remove leading '- ' or '* '
        item_text = " ".join(item_text.split())  # normalize spaces
        html_children = text_to_children(item_text)
        li_nodes.append(ParentNode("li", html_children))
    return ParentNode("ul", li_nodes)

def ordered_list_to_html_node(block) -> HTMLNode:
    lines = block.split("\n")
    li_nodes: list[HTMLNode] = []
    for line in lines:
        if line.strip() == "":
            continue
        line = line.lstrip()
        _, item_text = line.split(". ", 1)  # remove "1. " / "2. " etc.
        item_text = " ".join(item_text.split())
        html_children = text_to_children(item_text)
        li_nodes.append(ParentNode("li", html_children))
    return ParentNode("ol", li_nodes)

def text_to_children(text: str) -> list[HTMLNode]:
    text_nodes: list[TextNode] = text_to_textnodes(text)
    html_children: list[HTMLNode] = []
    for text_node in text_nodes:
        html_children.append(text_node_to_html_node(text_node))
    return html_children

def extract_title(markdown: str) -> str:
    lines = markdown.split("\n")
    for line in lines:
        new_line = line.strip()
        if new_line.startswith("# "):
            return new_line[2:].strip()
    raise ValueError("No level 1 heading found in the markdown.")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, 'r') as file_object:
        md_content = file_object.read()
    with open(template_path, 'r') as template_file:
        template_content = template_file.read()
    md_htmlnode = markdown_to_html_node(md_content)
    md_html = md_htmlnode.to_html()
    title = extract_title(md_content)
    final_html = template_content.replace("{{ Title }}", title)
    final_html = final_html.replace("{{ Content }}", md_html)
    dest_abs: str = os.path.dirname(dest_path)
    os.makedirs(dest_abs, exist_ok=True)
    with open(dest_path, 'w') as file_object:
        file_object.write(final_html)




def main():
    print(f"{extract_title("# Hello")}\n\n")
    print(f"{extract_title("## Not a title\n# Real Title\nSome text")}\n\n")
    print(f"{extract_title("There is no h1")}\n\n")
    

if __name__ == "__main__":
    main()