import unittest

from markdown_blocks import markdown_to_blocks, block_to_block_type
from blocknode import BlockType

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks_basic(self):
        markdown = "This is the first paragraph.\n\nThis is the second paragraph."
        expected = ["This is the first paragraph.", "This is the second paragraph."]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_markdown_to_blocks_single_block(self):
        markdown = "This is a single paragraph."
        expected = ["This is a single paragraph."]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_markdown_to_blocks_empty_string(self):
        markdown = ""
        expected = []
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_markdown_to_blocks_only_whitespace(self):
        markdown = "   \n\n   \n\n   "
        expected = []
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_markdown_to_blocks_multiple_empty_blocks(self):
        markdown = "First\n\n\n\nSecond"
        expected = ["First", "Second"]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_markdown_to_blocks_with_leading_trailing_whitespace(self):
        markdown = "  First paragraph  \n\n  Second paragraph  "
        expected = ["First paragraph", "Second paragraph"]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_markdown_to_blocks_single_newlines(self):
        markdown = "First line\nSecond line\n\nThird paragraph"
        expected = ["First line\nSecond line", "Third paragraph"]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_markdown_to_blocks_starting_with_newlines(self):
        markdown = "\n\nFirst paragraph"
        expected = ["First paragraph"]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_markdown_to_blocks_ending_with_newlines(self):
        markdown = "First paragraph\n\n"
        expected = ["First paragraph"]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_markdown_to_blocks_heading_and_paragraph(self):
        markdown = "# Heading 1\n\nThis is a paragraph under the heading."
        expected = ["# Heading 1", "This is a paragraph under the heading."]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_markdown_to_blocks_multiple_headings_and_paragraphs(self):
        markdown = "# H1\n\nFirst paragraph.\n\n## H2\n\nSecond paragraph."
        expected = ["# H1", "First paragraph.", "## H2", "Second paragraph."]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_markdown_to_blocks_unordered_list_block(self):
        markdown = "- item 1\n- item 2\n- item 3"
        expected = ["- item 1\n- item 2\n- item 3"]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_markdown_to_blocks_ordered_list_block(self):
        markdown = "1. first\n2. second\n3. third"
        expected = ["1. first\n2. second\n3. third"]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_markdown_to_blocks_paragraph_then_list(self):
        markdown = "Intro paragraph.\n\n- item 1\n- item 2"
        expected = ["Intro paragraph.", "- item 1\n- item 2"]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_markdown_to_blocks_code_block_fenced(self):
        markdown = "```python\nprint('hello')\nprint('world')\n```"
        expected = ["```python\nprint('hello')\nprint('world')\n```"]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_markdown_to_blocks_code_block_and_paragraph(self):
        markdown = "```python\nprint('hello')\n```\n\nAfter code."
        expected = ["```python\nprint('hello')\n```", "After code."]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_markdown_to_blocks_blank_lines_with_spaces_as_separators(self):
        markdown = "First\n\n   \nSecond"
        expected = ["First", "Second"]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_markdown_to_blocks_mixed_markdown(self):
        markdown = "# Title\n\nIntro paragraph.\n\n- item 1\n- item 2\n\n```js\nconsole.log('hi');\n```"
        expected = [
            "# Title",
            "Intro paragraph.",
            "- item 1\n- item 2",
            "```js\nconsole.log('hi');\n```",
        ]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_markdown_to_blocks_non_string_raises_type_error(self):
        with self.assertRaises(TypeError):
            markdown_to_blocks(None)  # type: ignore[arg-type]


class TestBlockToBlockType(unittest.TestCase):
    # --------- HEADING HAPPY PATHS ---------

    def test_heading_level_1(self):
        block = "# Heading 1"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading_level_3(self):
        block = "### Subheading level 3"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading_level_6(self):
        block = "###### Deep heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    # --------- HEADING EDGE CASES ---------

    def test_heading_too_many_hashes_is_not_heading(self):
        block = "####### Not a valid heading"  # 7 #
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading_without_space_after_hash_is_paragraph(self):
        block = "#NoSpaceHeading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading_only_hashes_is_paragraph(self):
        block = "######"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # --------- QUOTE HAPPY PATHS ---------

    def test_block_quote_basic(self):
        block = "> This is a quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    # --------- QUOTE EDGE CASES ---------

    def test_block_quote_missing_space_is_paragraph(self):
        block = ">Quote without space"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # --------- UNORDERED LIST HAPPY PATHS ---------

    def test_unordered_list_dash(self):
        block = "- item 1"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_star(self):
        block = "* item 1"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    # --------- UNORDERED LIST EDGE CASES ---------

    def test_unordered_list_missing_space_after_bullet_is_paragraph(self):
        block = "-item without space"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # --------- ORDERED LIST HAPPY PATHS ---------

    def test_ordered_list_single_digit(self):
        block = "1. first item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_multiple_digits(self):
        block = "23. item number 23"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    # --------- ORDERED LIST EDGE CASES ---------

    def test_ordered_list_missing_space_after_dot_is_paragraph(self):
        block = "1.second item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_just_number_and_dot_is_paragraph(self):
        block = "3."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # --------- CODE BLOCK HAPPY PATHS ---------

    def test_code_block_triple_backticks(self):
        block = "```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_block_with_language(self):
        block = "```python"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    # --------- PARAGRAPH / DEFAULT CASES ---------

    def test_plain_paragraph_text(self):
        block = "This is just some text."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_plain_paragraph_with_leading_spaces(self):
        block = "   This is also just text."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_empty_string_is_paragraph(self):
        # Depending on your design, you might treat this as paragraph or handle earlier.
        # Here we assume the function still returns PARAGRAPH for empty strings.
        block = ""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_whitespace_only_is_paragraph(self):
        block = "    "
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # --------- VALIDATION / ERROR CASES ---------

    def test_block_to_block_type_non_string_raises_type_error(self):
        with self.assertRaises(TypeError):
            block_to_block_type(None)  # type: ignore[arg-type]

        with self.assertRaises(TypeError):
            block_to_block_type(123)  # type: ignore[arg-type]

if __name__ == "__main__":
    unittest.main()

