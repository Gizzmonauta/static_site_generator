import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_nodes_with_different_text(self):
        node1 = TextNode("A", TextType.BOLD)
        node2 = TextNode("B", TextType.BOLD)
        self.assertNotEqual(node1, node2)

    def test_nodes_with_different_type(self):
        node1 = TextNode("A", TextType.BOLD)
        node2 = TextNode("A", TextType.ITALIC)
        self.assertNotEqual(node1, node2)

    def test_nodes_with_different_url(self):
        node1 = TextNode("A", TextType.LINK, "https://example.com/1")
        node2 = TextNode("A", TextType.LINK)
        self.assertNotEqual(node1, node2)

    def test_both_urls_none(self):
        node1 = TextNode("A", TextType.LINK, None)
        node2 = TextNode("A", TextType.LINK, None)
        self.assertEqual(node1, node2)

if __name__ == "__main__":
    unittest.main()