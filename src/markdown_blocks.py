import re
from blocknode import BlockType

def markdown_to_blocks(markdown: str) -> list[BlockType]:
    """
    Convert a markdown string into a list of blocks.
    Currently, only inline markdown is supported, so the entire markdown string
    is converted into a single paragraph block containing TextNodes.
    """
    if not isinstance(markdown, str):
        raise TypeError("Input must be a string")
    
    new_blocks: list[BlockType] = []
    lines = markdown.split("\n\n")
    for line in lines:
        line = line.strip()
        if not line:
            continue
        new_blocks.append(line)

    return new_blocks

def block_to_block_type(block: str) -> BlockType:
    """
    Determine the BlockType of a given block of markdown text.
    """
    if not isinstance(block, str):
        raise TypeError("Block must be a string")
    
    # Heading: 1–6 hashes + space
    if re.match(r"^#{1,6}\s+", block):
        return BlockType.HEADING

    # Block quote
    if re.match(r"^>\s+", block):
        return BlockType.QUOTE

    # Unordered list (- or *)
    if re.match(r"^[-*]\s+", block):
        return BlockType.UNORDERED_LIST

    # Ordered list (digits.)
    if re.match(r"^\d+\.\s+", block):
        return BlockType.ORDERED_LIST

    # Code block (```...)
    if re.match(r"^```+", block):
        return BlockType.CODE

    # Fallback → paragraph
    return BlockType.PARAGRAPH
    


def main():
    markdown_text = '''

# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.




- This is the first list item in a list block
- This is a list item
- This is another list item

'''
    blocks = markdown_to_blocks(markdown_text)
    print(blocks)
    
    text = "## Sample Heading"
    print(f"Block type of '{text}': {block_to_block_type(text)}")

    text = "> This is a block quote."
    print(f"Block type of '{text}': {block_to_block_type(text)}")

    text = "- List item one"
    print(f"Block type of '{text}': {block_to_block_type(text)}")

    text = "1. First ordered item"
    print(f"Block type of '{text}': {block_to_block_type(text)}")

    text = "```python\nprint('Hello, World!')\n```"
    print(f"Block type of '{text}': {block_to_block_type(text)}")

    text = "Just a regular paragraph."
    print(f"Block type of '{text}': {block_to_block_type(text)}")

    text = "   "
    print(f"Block type of '{text}': {block_to_block_type(text)}")

    text = "####### Too many hashes"
    print(f"Block type of '{text}': {block_to_block_type(text)}")

    text = "##NoSpaces"
    print(f"Block type of '{text}': {block_to_block_type(text)}")

if __name__ == "__main__":
    main()