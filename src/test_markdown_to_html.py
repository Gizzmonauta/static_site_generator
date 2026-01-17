import unittest
from markdown_to_html import extract_title, markdown_to_html_node
from htmlnode import HTMLNode

class TestMarkdownToHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_paragraph_single_line(self):
        md = "Hello world"
        node = markdown_to_html_node(md)
        self.assertEqual(node.to_html(), "<div><p>Hello world</p></div>")

    def test_paragraph_whitespace_collapse(self):
        md = "Hello     world"
        node = markdown_to_html_node(md)
        self.assertEqual(node.to_html(), "<div><p>Hello world</p></div>")

    def test_paragraph_inline_markdown(self):
        md = "Hi **Bob** and _Ann_ with `code`"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><p>Hi <b>Bob</b> and <i>Ann</i> with <code>code</code></p></div>",
        )

    def test_empty_markdown_returns_empty_div(self):
        md = "   \n\n   "
        node = markdown_to_html_node(md)
        self.assertEqual(node.to_html(), "<div></div>")

    def test_heading_h1(self):
        md = "# Title"
        node = markdown_to_html_node(md)
        self.assertEqual(node.to_html(), "<div><h1>Title</h1></div>")

    def test_heading_h3_with_inline(self):
        md = "### Hello **world**"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><h3>Hello <b>world</b></h3></div>",
        )

    def test_heading_h6(self):
        md = "###### Max"
        node = markdown_to_html_node(md)
        self.assertEqual(node.to_html(), "<div><h6>Max</h6></div>")

    def test_codeblock_dedent_common_indent(self):
        md = """
    ```
        line one
        line two
    ```
    """
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><pre><code>line one\nline two\n</code></pre></div>",
        )

    def test_codeblock_preserves_relative_indent(self):
        md = """
    ```
    def f():
        return 1
    ```
    """
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><pre><code>def f():\n    return 1\n</code></pre></div>",
        )

    def test_codeblock_no_inline_parsing(self):
        md = "```\nthis is **not bold** and _not italic_\n```"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><pre><code>this is **not bold** and _not italic_\n</code></pre></div>",
        )

    def test_quote_block(self):
        md = """
    > This is a quote
    > with **bold** and _italic_
    """
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><blockquote>This is a quote with <b>bold</b> and <i>italic</i></blockquote></div>",
        )

    def test_quote_single_line(self):
        md = "> Quote with `code`"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><blockquote>Quote with <code>code</code></blockquote></div>",
        )

    def test_unordered_list(self):
        md = """
    - Item one
    - Item two with **bold**
    - Item three
    """
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><ul>"
            "<li>Item one</li>"
            "<li>Item two with <b>bold</b></li>"
            "<li>Item three</li>"
            "</ul></div>",
        )

    def test_unordered_list_with_asterisks(self):
        md = """
    * First
    * Second with _italic_
    """
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><ul>"
            "<li>First</li>"
            "<li>Second with <i>italic</i></li>"
            "</ul></div>",
        )

    def test_ordered_list(self):
        md = """
    1. First
    2. Second with **bold**
    3. Third
    """
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><ol>"
            "<li>First</li>"
            "<li>Second with <b>bold</b></li>"
            "<li>Third</li>"
            "</ol></div>",
        )

    def test_ordered_list_with_indentation(self):
        md = """
        1. One
        2. Two
        """
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><ol><li>One</li><li>Two</li></ol></div>",
        )

    def test_extract_title_basic_happy_path(self):
        self.assertEqual(extract_title("# Hello"), "Hello")
    
    
    def test_extract_title_multiple_headings(self):
        self.assertEqual(extract_title("## Not a title\n# Real Title\nSome text"), "Real Title")
    
    def test_extract_title_no_h1(self):
        with self.assertRaises(ValueError):
            extract_title("There is no h1")
    
    def test_extract_title_with_whitespace_before_hash(self):
        self.assertEqual(extract_title("   # Hello"), "Hello")
    
    def test_extract_title_multiple_h1_stops_at_first(self):
        self.assertEqual(extract_title("# First Title\n# Second Title\nSome text"), "First Title")