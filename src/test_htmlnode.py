import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHtmlNode(unittest.TestCase):

    # This test evaluates the equality operator for HTMLNode instances
    def test_eq(self):
        node1 = HTMLNode(tag="div", value="Hello", children=[], props={"class": "greeting"})
        node2 = HTMLNode(tag="div", value="Hello", children=[], props={"class": "greeting"})
        self.assertEqual(node1, node2)

    # This test evaluates the equality operator for HTMLNode instances with different tags
    def test_nodes_with_different_tag(self):
        node1 = HTMLNode(tag="div")
        node2 = HTMLNode(tag="span")
        self.assertNotEqual(node1, node2)

    # Tests equality operator for HTMLNode instances with different values
    def test_nodes_with_different_value(self):
        node1 = HTMLNode(tag="div", value="Hello")
        node2 = HTMLNode(tag="div", value="World")
        self.assertNotEqual(node1, node2)

    # Tests that props_to_html returns an empty string when props is None
    def test_props_to_html_none(self):
        node = HTMLNode(tag="a", props=None)
        self.assertEqual(node.props_to_html(), "")

    # Tests that props_to_html returns an empty string when props is an empty dict
    def test_props_to_html_empty(self):
        node = HTMLNode(tag="a", props={})
        self.assertEqual(node.props_to_html(), "")

    # Tests that props_to_html returns the correct string for a single attribute
    def test_props_to_html_single(self):
        node = HTMLNode(tag="a", props={"href": "https://a.com"})
        self.assertEqual(node.props_to_html(), ' href="https://a.com"')

    # Tests that props_to_html returns all attributes correctly for multiple attributes
    def test_props_to_html_multiple(self):
        node = HTMLNode(tag="a", props={"href": "x", "target": "_blank"})
        result = node.props_to_html()
        self.assertIn('href="x"', result)
        self.assertIn('target="_blank"', result)
        self.assertTrue(result.startswith(" ") and " " in result.strip())

    # Tests that __repr__ returns a string containing all relevant fields
    def test_repr(self):
        node = HTMLNode(tag="p", value="text", children=None, props={"id": "main"})
        rep = repr(node)
        self.assertIn("HTMLNode", rep)
        self.assertIn("p", rep)
        self.assertIn("text", rep)
        self.assertIn("id", rep)

    # Tests that a node with only a value sets value and leaves children as None
    def test_node_only_value(self):
        node = HTMLNode(value="text")
        self.assertEqual(node.value, "text")
        self.assertIsNone(node.children)

    # Tests that a node with only children sets children and leaves value as None
    def test_node_only_children(self):
        child = HTMLNode(tag="span")
        node = HTMLNode(children=[child])
        self.assertEqual(node.children, [child])
        self.assertIsNone(node.value)

    # Tests that a node with both value and children sets both fields correctly
    def test_node_both_value_and_children(self):
        child = HTMLNode(tag="span")
        node = HTMLNode(value="text", children=[child])
        self.assertEqual(node.value, "text")
        self.assertEqual(node.children, [child])

    # Tests that a node with neither value nor children has both fields as None
    def test_node_neither_value_nor_children(self):
        node = HTMLNode()
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)

    # Tests that nested children are correctly stored, assigned and accessible
    def test_nested_children(self):
        child = HTMLNode(tag="span", value="child")
        parent = HTMLNode(tag="div", children=[child])
        self.assertEqual(parent.children[0], child)

    # Tests that props_to_html handles special characters and empty attribute values
    def test_props_special_characters(self):
        node = HTMLNode(tag="a", props={"data-info": "a&b<c>d", "empty": ""})
        result = node.props_to_html()
        self.assertIn('data-info="a&b<c>d"', result)
        self.assertIn('empty=""', result)

    # Tests that a LeafNode renders a standard paragraph tag correctly
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    # Tests that a LeafNode renders an anchor tag with attributes correctly
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    # Tests that a LeafNode with no tag renders raw text
    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    # Tests that a LeafNode without a value raises a ValueError
    def test_leaf_to_html_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    # Tests that LeafNode constructor raises TypeError if children are passed
    def test_leaf_constructor_with_children(self):
        with self.assertRaises(TypeError):
            LeafNode(tag="p", value="text", children=[])

    # Tests that a ParentNode with leaf children renders correctly
    def test_parent_to_html_simple(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i></p>",
        )

    # Tests that a ParentNode with nested ParentNode children renders correctly
    def test_parent_to_html_nested(self):
        node = ParentNode(
            "div",
            [
                ParentNode("p", [LeafNode("b", "Bold text")]),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<div><p><b>Bold text</b></p>Normal text</div>",
        )

    # Tests that a ParentNode without a tag raises a ValueError
    def test_parent_to_html_no_tag(self):
        node = ParentNode(None, [LeafNode("b", "Bold text")])
        with self.assertRaises(ValueError):
            node.to_html()

    # Tests that a ParentNode without children raises a ValueError
    def test_parent_to_html_no_children(self):
        node = ParentNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    # Tests that a ParentNode with a single leaf child renders correctly
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    # Tests that a ParentNode with grandchildren (deep nesting) renders correctly
    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    # Tests a complex structure with multiple nested parents and leaf nodes
    def test_parent_to_html_complex(self):
        grandchild = LeafNode("b", "grandchild")
        child1 = ParentNode("span", [grandchild, grandchild])
        child2 = ParentNode("span", [grandchild, grandchild])
        leaf = LeafNode("i", "leaf")
        parent = ParentNode("div", [child1, child2, leaf, leaf, leaf])
        self.assertEqual(
            parent.to_html(),
            "<div><span><b>grandchild</b><b>grandchild</b></span><span><b>grandchild</b><b>grandchild</b></span><i>leaf</i><i>leaf</i><i>leaf</i></div>",
        )

if __name__ == "__main__":
    unittest.main()