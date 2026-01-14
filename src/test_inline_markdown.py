import unittest
import re

from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_link, split_nodes_image, text_to_textnodes

class TestCreateTextNodes(unittest.TestCase):
    def test_split_nodes_delimiter_empty_old_nodes(self):
        result = split_nodes_delimiter([], "**", TextType.BOLD)
        self.assertEqual(result, [])

    def test_split_nodes_delimiter_old_nodes_contains_none(self):
        with self.assertRaises(TypeError):
            split_nodes_delimiter([None], "**", TextType.BOLD)

    def test_split_nodes_delimiter_old_nodes_contains_non_textnode(self):
        with self.assertRaises(TypeError):
            split_nodes_delimiter(["not a TextNode"], "**", TextType.BOLD)

    def test_split_nodes_delimiter_delimiter_is_none(self):
        with self.assertRaises(TypeError):
            split_nodes_delimiter([TextNode("text", TextType.TEXT)], None, TextType.BOLD)

    def test_split_nodes_delimiter_text_type_is_none(self):
        with self.assertRaises(TypeError):
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
        with self.assertRaises(TypeError):
            split_nodes_delimiter("not a list", "**", TextType.BOLD)

    def test_validate_split_nodes_delimiter_args_invalid_delimiter(self):
        with self.assertRaises(TypeError):
            split_nodes_delimiter([TextNode("text", TextType.TEXT)], "", TextType.BOLD)

    def test_validate_split_nodes_delimiter_args_invalid_text_type(self):
        with self.assertRaises(TypeError):
            split_nodes_delimiter([TextNode("text", TextType.TEXT)], "**", "not a text type")

    def test_validate_split_nodes_delimiter_args_unmatched_delimiter(self):
        with self.assertRaises(ValueError):
            split_nodes_delimiter(
                [TextNode("This is **bold text", TextType.TEXT)],
                "**",
                TextType.BOLD
            )

    def test_extract_markdown_images_with_only_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected = [('rick roll', 'https://i.imgur.com/aKaOqIh.gif'), ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_images_consecutive_images(self):
        text = '![John](https://www.john.com)![Mary](https://www.mary.com)![Jerry](https://www.jerry.com)'
        expected = [('John', 'https://www.john.com'), ('Mary', 'https://www.mary.com'), ('Jerry', 'https://www.jerry.com')]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_images_broken_link_exclusion(self):
        # The parenthesis in jer(r)y.com breaks the strict regex match, so Jerry is excluded
        text = '![John](https://www.john.com)![Mary](https://www.mary.com)![Jerry](https://www.jer(r)y.com)'
        expected = [('John', 'https://www.john.com'), ('Mary', 'https://www.mary.com')]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_images_recovery_after_broken_link(self):
        # Jerry is skipped, but the regex engine recovers to find Jessica
        text = '![John](https://www.john.com)![Mary](https://www.mary.com)![Jerry](https://www.jer(r)y.com)![Jessica](https://jessica.com)'
        expected = [('John', 'https://www.john.com'), ('Mary', 'https://www.mary.com'), ('Jessica', 'https://jessica.com')]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_images_with_links(self):
        text = '[John](https://www.john.com)![Mary](https://www.mary.com)![Jerry](https://www.jerry.com)'
        expected = [('Mary', 'https://www.mary.com'), ('Jerry', 'https://www.jerry.com')]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_links_with_only_links_multiple(self):
        from inline_markdown import extract_markdown_links
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        expected = [('to boot dev', 'https://www.boot.dev'), ('to youtube', 'https://www.youtube.com/@bootdotdev')]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_extract_markdown_links_with_image(self):
        from inline_markdown import extract_markdown_links
        text = "This is text with a link [to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)"
        expected = [('to boot dev', 'https://www.boot.dev')]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_extract_markdown_images_empty_alt(self):
        text = "![   ](https://example.com/image.png)"
        expected = [('   ', 'https://example.com/image.png')]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_images_empty_url(self):
        text = "![alt]()"
        expected = [('alt', '')]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_images_spaces_in_url(self):
        text = "![alt](https://example.com/image file.png)"
        expected = [('alt', 'https://example.com/image file.png')]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_images_special_characters_in_alt(self):
        text = "![a!@# $%^&*()_+](https://example.com/img.png)"
        expected = [('a!@# $%^&*()_+', 'https://example.com/img.png')]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_images_at_start_and_end(self):
        text = "![start](https://start.com) text ![end](https://end.com)"
        expected = [('start', 'https://start.com'), ('end', 'https://end.com')]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_images_none_present(self):
        text = "This text has no images."
        expected = []
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_links_empty_text(self):
        text = "[](https://example.com)"
        expected = [('', 'https://example.com')]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_extract_markdown_links_empty_url(self):
        text = "[text]()"
        expected = [('text', '')]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_extract_markdown_links_spaces_in_url(self):
        text = "[text](https://example.com/page one)"
        expected = [('text', 'https://example.com/page one')]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_extract_markdown_links_at_start_and_end(self):
        text = "[start](https://start.com) text [end](https://end.com)"
        expected = [('start', 'https://start.com'), ('end', 'https://end.com')]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_extract_markdown_links_none_present(self):
        text = "This text has no links."
        expected = []
        self.assertEqual(extract_markdown_links(text), expected)

    def test_extract_markdown_links_nested_brackets(self):
        text = "[text [inner]](https://example.com)"
        expected = []
        self.assertEqual(extract_markdown_links(text), expected)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_nodes_image_with_text_bold_links_images(self):
        nodes = [
            TextNode("This has `code`", TextType.TEXT),
            TextNode("already bold", TextType.BOLD),
            TextNode("This also has `code` in it", TextType.TEXT),
            TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT),
            TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT),
            TextNode('[John](https://www.john.com)![Mary](https://www.mary.com)![Jerry](https://www.jerry.com)', TextType.TEXT)
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("This has `code`", TextType.TEXT),
                TextNode("already bold", TextType.BOLD),
                TextNode("This also has `code` in it", TextType.TEXT),
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
                TextNode(" and ", TextType.TEXT),
                TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT),
                TextNode("[John](https://www.john.com)", TextType.TEXT),
                TextNode("Mary", TextType.IMAGE, "https://www.mary.com"),
                TextNode("Jerry", TextType.IMAGE, "https://www.jerry.com"),
            ],
            new_nodes,
        )

    def test_split_nodes_link_with_text_bold_links_images(self):
        nodes = [
            TextNode("This has `code`", TextType.TEXT),
            TextNode("already bold", TextType.BOLD),
            TextNode("This also has `code` in it", TextType.TEXT),
            TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT),
            TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT),
            TextNode('[John](https://www.john.com)![Mary](https://www.mary.com)![Jerry](https://www.jerry.com)', TextType.TEXT)
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(
            [
                TextNode("This has `code`", TextType.TEXT),
                TextNode("already bold", TextType.BOLD),
                TextNode("This also has `code` in it", TextType.TEXT),
                TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT),
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
                TextNode("John", TextType.LINK, "https://www.john.com"),
                TextNode("![Mary](https://www.mary.com)![Jerry](https://www.jerry.com)", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_nodes_image_empty_list(self):
        self.assertListEqual([], split_nodes_image([]))

    def test_split_nodes_link_empty_list(self):
        self.assertListEqual([], split_nodes_link([]))


    def test_split_nodes_image_text_without_images_unchanged(self):
        node = TextNode("Just plain text, nothing here.", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_nodes_link_text_without_links_unchanged(self):
        node = TextNode("Just plain text, nothing here.", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_nodes_image_only_image_node(self):
        node = TextNode("![alt](https://example.com/img.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("alt", TextType.IMAGE, "https://example.com/img.png"),
            ],
            new_nodes,
        )

    def test_split_nodes_link_only_link_node(self):
        node = TextNode("[boot](https://www.boot.dev)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("boot", TextType.LINK, "https://www.boot.dev"),
            ],
            new_nodes,
        )

    def test_split_nodes_image_back_to_back_images(self):
        node = TextNode(
            "Before ![one](https://example.com/1.png)![two](https://example.com/2.png) after",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Before ", TextType.TEXT),
                TextNode("one", TextType.IMAGE, "https://example.com/1.png"),
                TextNode("two", TextType.IMAGE, "https://example.com/2.png"),
                TextNode(" after", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_nodes_link_back_to_back_links(self):
        node = TextNode(
            "Before [one](https://example.com/1)[two](https://example.com/2) after",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Before ", TextType.TEXT),
                TextNode("one", TextType.LINK, "https://example.com/1"),
                TextNode("two", TextType.LINK, "https://example.com/2"),
                TextNode(" after", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_nodes_image_does_not_touch_existing_image_nodes(self):
        nodes = [
            TextNode("before ![alt](https://example.com/img.png)", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "https://example.com/other.png"),
        ]
        new_nodes = split_nodes_image(nodes)
        # First node is split, second one is preserved as-is
        self.assertListEqual(
            [
                TextNode("before ", TextType.TEXT),
                TextNode("alt", TextType.IMAGE, "https://example.com/img.png"),
                TextNode("alt", TextType.IMAGE, "https://example.com/other.png"),
            ],
            new_nodes,
        )

    def test_split_nodes_link_does_not_touch_existing_link_nodes(self):
        nodes = [
            TextNode("before [boot](https://www.boot.dev)", TextType.TEXT),
            TextNode("boot", TextType.LINK, "https://www.other.dev"),
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(
            [
                TextNode("before ", TextType.TEXT),
                TextNode("boot", TextType.LINK, "https://www.boot.dev"),
                TextNode("boot", TextType.LINK, "https://www.other.dev"),
            ],
            new_nodes,
        )

    def test_split_nodes_image_invalid_markdown_unchanged(self):
        # Broken image syntax: missing closing parenthesis
        node = TextNode("This looks like ![an image](https://example.com/img.png", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)


    def test_split_nodes_link_invalid_markdown_unchanged(self):
        # Broken link syntax: missing closing parenthesis
        node = TextNode("This looks like [a link](https://example.com/link", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_nodes_image_raises_on_non_list(self):
        with self.assertRaises(TypeError):
            split_nodes_image(None)  # type: ignore[arg-type]


    def test_split_nodes_link_raises_on_non_list(self):
        with self.assertRaises(TypeError):
            split_nodes_link("not a list")  # type: ignore[arg-type]


    def test_split_nodes_image_raises_on_non_textnode_elements(self):
        with self.assertRaises(TypeError):
            split_nodes_image(["not a TextNode"])  # type: ignore[list-item]


    def test_split_nodes_link_raises_on_non_textnode_elements(self):
        with self.assertRaises(TypeError):
            split_nodes_link([123])  # type: ignore[list-item]

    def test_split_nodes_image_then_link_pipeline(self):
        nodes = [
            TextNode(
                "Text ![img](https://example.com/img.png) and [link](https://example.com)",
                TextType.TEXT,
            )
        ]

        # First split images
        after_images = split_nodes_image(nodes)
        # Then split links on the result
        final_nodes = split_nodes_link(after_images)

        self.assertListEqual(
            [
                TextNode("Text ", TextType.TEXT),
                TextNode("img", TextType.IMAGE, "https://example.com/img.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
            ],
            final_nodes,
        )

    def test_text_to_textnodes_basic_bold_asterisks(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode('This is ', TextType.TEXT),
            TextNode('text', TextType.BOLD),
            TextNode(' with an ', TextType.TEXT),
            TextNode('italic', TextType.ITALIC),
            TextNode(' word and a ', TextType.TEXT),
            TextNode('code block', TextType.CODE),
            TextNode(' and an ', TextType.TEXT),
            TextNode('obi wan image', TextType.IMAGE, 'https://i.imgur.com/fJRm4Vk.jpeg'),
            TextNode(' and a ', TextType.TEXT),
            TextNode('link', TextType.LINK, 'https://boot.dev')
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_text_to_textnodes_basic_bold_underscores(self):
        text = "This is __text__ with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode('This is ', TextType.TEXT),
            TextNode('text', TextType.BOLD),
            TextNode(' with an ', TextType.TEXT),
            TextNode('italic', TextType.ITALIC),
            TextNode(' word and a ', TextType.TEXT),
            TextNode('code block', TextType.CODE),
            TextNode(' and an ', TextType.TEXT),
            TextNode('obi wan image', TextType.IMAGE, 'https://i.imgur.com/fJRm4Vk.jpeg'),
            TextNode(' and a ', TextType.TEXT),
            TextNode('link', TextType.LINK, 'https://boot.dev')
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_text_to_textnodes_basic_italic_asterisks(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode('This is ', TextType.TEXT),
            TextNode('text', TextType.BOLD),
            TextNode(' with an ', TextType.TEXT),
            TextNode('italic', TextType.ITALIC),
            TextNode(' word and a ', TextType.TEXT),
            TextNode('code block', TextType.CODE),
            TextNode(' and an ', TextType.TEXT),
            TextNode('obi wan image', TextType.IMAGE, 'https://i.imgur.com/fJRm4Vk.jpeg'),
            TextNode(' and a ', TextType.TEXT),
            TextNode('link', TextType.LINK, 'https://boot.dev')
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_text_to_textnodes_basic_italic_underscores(self):
        text = "This is __text__ with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode('This is ', TextType.TEXT),
            TextNode('text', TextType.BOLD),
            TextNode(' with an ', TextType.TEXT),
            TextNode('italic', TextType.ITALIC),
            TextNode(' word and a ', TextType.TEXT),
            TextNode('code block', TextType.CODE),
            TextNode(' and an ', TextType.TEXT),
            TextNode('obi wan image', TextType.IMAGE, 'https://i.imgur.com/fJRm4Vk.jpeg'),
            TextNode(' and a ', TextType.TEXT),
            TextNode('link', TextType.LINK, 'https://boot.dev')
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_text_to_textnodes_bold_italic_asterisks(self):
        text = "This is ***bold + italic*** text with a __bold__ with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode('This is ', TextType.TEXT),
            TextNode('bold + italic', TextType.BOLD_ITALIC),
            TextNode(' text with a ', TextType.TEXT),
            TextNode('bold', TextType.BOLD),
            TextNode(' with an ', TextType.TEXT),
            TextNode('italic', TextType.ITALIC),
            TextNode(' word and a ', TextType.TEXT),
            TextNode('code block', TextType.CODE),
            TextNode(' and an ', TextType.TEXT),
            TextNode('obi wan image', TextType.IMAGE, 'https://i.imgur.com/fJRm4Vk.jpeg'),
            TextNode(' and a ', TextType.TEXT),
            TextNode('link', TextType.LINK, 'https://boot.dev')
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_text_to_textnodes_bold_italic_underscores(self):
        text = "This is ___bold + italic___ text with a __bold__ word, an _italic_ word and a `code block`. Also,an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode('This is ', TextType.TEXT),
            TextNode('bold + italic', TextType.BOLD_ITALIC),
            TextNode(' text with a ', TextType.TEXT),
            TextNode('bold', TextType.BOLD),
            TextNode(' word, an ', TextType.TEXT),
            TextNode('italic', TextType.ITALIC),
            TextNode(' word and a ', TextType.TEXT),
            TextNode('code block', TextType.CODE),
            TextNode('. Also,an ', TextType.TEXT),
            TextNode('obi wan image', TextType.IMAGE, 'https://i.imgur.com/fJRm4Vk.jpeg'),
            TextNode(' and a ', TextType.TEXT),
            TextNode('link', TextType.LINK, 'https://boot.dev')
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_text_to_textnodes_empty_string(self):
        text = ""
        expected = [TextNode("", TextType.TEXT)]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_text_to_textnodes_plain_text(self):
        text = "This is plain text with no markdown."
        expected = [TextNode("This is plain text with no markdown.", TextType.TEXT)]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_text_to_textnodes_unmatched_delimiter(self):
        text = "This is **bold text"
        with self.assertRaises(ValueError):
            text_to_textnodes(text)

    def test_text_to_textnodes_delimiter_at_start(self):
        text = "**bold** at start"
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode(" at start", TextType.TEXT)
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_text_to_textnodes_delimiter_at_end(self):
        text = "Text at end **bold**"
        expected = [
            TextNode("Text at end ", TextType.TEXT),
            TextNode("bold", TextType.BOLD)
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_text_to_textnodes_empty_formatted_section(self):
        text = "Empty **bold** section"
        expected = [
            TextNode("Empty ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" section", TextType.TEXT)
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_text_to_textnodes_code_with_backticks_inside(self):
        text = "Code `with 'quote'` inside"
        expected = [
            TextNode("Code ", TextType.TEXT),
            TextNode("with 'quote'", TextType.CODE),
            TextNode(" inside", TextType.TEXT)
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_text_to_textnodes_image_with_special_chars(self):
        text = "Image ![alt text with spaces & symbols!@#](https://example.com/image.jpg)"
        expected = [
            TextNode("Image ", TextType.TEXT),
            TextNode("alt text with spaces & symbols!@#", TextType.IMAGE, "https://example.com/image.jpg")
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_text_to_textnodes_link_with_special_chars(self):
        text = "Link [text with spaces & symbols!@#](https://example.com/page?query=value)"
        expected = [
            TextNode("Link ", TextType.TEXT),
            TextNode("text with spaces & symbols!@#", TextType.LINK, "https://example.com/page?query=value")
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_text_to_textnodes_bold_italic_at_start(self):
        text = "***bold italic*** start"
        expected = [
            TextNode("bold italic", TextType.BOLD_ITALIC),
            TextNode(" start", TextType.TEXT)
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_text_to_textnodes_multiple_bold_italic(self):
        text = "***first*** and ***second***"
        expected = [
            TextNode("first", TextType.BOLD_ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("second", TextType.BOLD_ITALIC)
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_text_to_textnodes_mixed_delimiters(self):
        text = "**bold _italic_**"
        expected = [
            TextNode("bold _italic_", TextType.BOLD)
        ]
        self.assertEqual(text_to_textnodes(text), expected)

if __name__ == "__main__":
    unittest.main()

