import unittest

from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter

class TestCreateTextNodes(unittest.TestCase):
    def test_split_nodes_delimiter_empty_old_nodes(self):
        result = split_nodes_delimiter([], "**", TextType.BOLD)
        self.assertEqual(result, [])

    def test_split_nodes_delimiter_old_nodes_contains_none(self):
        with self.assertRaises(ValueError):
            split_nodes_delimiter([None], "**", TextType.BOLD)

    def test_split_nodes_delimiter_old_nodes_contains_non_textnode(self):
        with self.assertRaises(ValueError):
            split_nodes_delimiter(["not a TextNode"], "**", TextType.BOLD)

    def test_split_nodes_delimiter_delimiter_is_none(self):
        with self.assertRaises(ValueError):
            split_nodes_delimiter([TextNode("text", TextType.TEXT)], None, TextType.BOLD)

    def test_split_nodes_delimiter_text_type_is_none(self):
        with self.assertRaises(ValueError):
            split_nodes_delimiter([TextNode("text", TextType.TEXT)], "**", None)

    def test_split_nodes_delimiter_basic(self):
        nodes = [TextNode("This is **bold** text", TextType.TEXT)]
        delimiter = "**"
        text_type = TextType.BOLD
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT)
        ]
        result = split_nodes_delimiter(nodes, delimiter, text_type)
        self.assertEqual(result, expected)

    def test_split_nodes_delimiter_delimiter_at_start(self):
        nodes = [TextNode("**bold** text", TextType.TEXT)]
        delimiter = "**"
        text_type = TextType.BOLD
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT)
        ]
        result = split_nodes_delimiter(nodes, delimiter, text_type)
        self.assertEqual(result, expected)

    def test_split_nodes_delimiter_delimiter_at_end(self):
        nodes = [TextNode("Text is **bold**", TextType.TEXT)]
        delimiter = "**"
        text_type = TextType.BOLD
        expected = [
            TextNode("Text is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
        ]
        result = split_nodes_delimiter(nodes, delimiter, text_type)
        self.assertEqual(result, expected)

    def test_split_nodes_delimiter_no_delimiter(self):
        nodes = [TextNode("This is plain text", TextType.TEXT)]
        delimiter = "**"
        text_type = TextType.BOLD
        expected = [TextNode("This is plain text", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, delimiter, text_type)
        self.assertEqual(result, expected)

    def test_split_nodes_delimiter_multiple_nodes(self):
        nodes = [
            TextNode("This has `code`", TextType.TEXT),
            TextNode("already bold", TextType.BOLD),
            TextNode("This also has `code` in it", TextType.TEXT)
        ]
        delimiter = "`"
        text_type = TextType.CODE
        expected = [
            TextNode("This has ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode("already bold", TextType.BOLD),
            TextNode("This also has ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" in it", TextType.TEXT)
        ]
        result = split_nodes_delimiter(nodes, delimiter, text_type)
        self.assertEqual(result, expected)

    def test_split_nodes_delimiter_same_string_after_split(self):
        node = TextNode("code `code` code", TextType.TEXT)
        expected = [
            TextNode("code ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" code", TextType.TEXT)
        ]
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, expected)

    def test_validate_split_nodes_delimiter_args_invalid_old_nodes(self):
        with self.assertRaises(ValueError):
            split_nodes_delimiter("not a list", "**", TextType.BOLD)

    def test_validate_split_nodes_delimiter_args_invalid_delimiter(self):
        with self.assertRaises(ValueError):
            split_nodes_delimiter([TextNode("text", TextType.TEXT)], "", TextType.BOLD)

    def test_validate_split_nodes_delimiter_args_invalid_text_type(self):
        with self.assertRaises(ValueError):
            split_nodes_delimiter([TextNode("text", TextType.TEXT)], "**", "not a text type")

    def test_validate_split_nodes_delimiter_args_unmatched_delimiter(self):
        with self.assertRaises(ValueError):
            split_nodes_delimiter(
                [TextNode("This is **bold text", TextType.TEXT)],
                "**",
                TextType.BOLD
            )

if __name__ == "__main__":
    unittest.main()