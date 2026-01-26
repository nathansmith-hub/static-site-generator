import unittest

from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links

from textnode import TextNode, TextType

class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_no_delim(self):
        node = TextNode("This is just text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [TextNode("This is just text", TextType.TEXT)],
            new_nodes,
        )

    def test_delim_bold_no_closing(self):
        node = TextNode("This is **bold text", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_delim_multiple_italic(self):
        node = TextNode("This is _italic_ text _too_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text ", TextType.TEXT),
                TextNode("too", TextType.ITALIC)
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is `code` text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_italic_skip_non_text_nodes(self):
        nodes = [
            TextNode("plain ", TextType.TEXT),
            TextNode("keep", TextType.BOLD),
            TextNode(" and _italic_", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("plain ", TextType.TEXT),
                TextNode("keep", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_extract_markdown_images_single(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_multi(self):
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)

    def test_extract_markdown_images_no_match(self):
        matches = extract_markdown_images("Just plain text, no images here.")
        self.assertListEqual([], matches)

    def test_extract_markdown_images_with_link(self):
        matches = "![alt](https://example.com/img.png) and [link](https://example.com)"
        self.assertListEqual(
            [("link", "https://example.com")],
            extract_markdown_links(matches),
        )

    def test_extract_markdown_images_no_alt(self):
        matches = extract_markdown_images("![](https://example.com/img.png)")
        self.assertListEqual([("", "https://example.com/img.png")], matches)

    def test_extract_markdown_links_single(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.boot.dev)"
        )
        self.assertListEqual([("link", "https://www.boot.dev")], matches)

    def test_extract_markdown_links_multi(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_extract_markdown_links_no_match(self):
        matches = extract_markdown_links("Just plain text, no links here.")
        self.assertListEqual([], matches)

    def test_extract_markdown_links_with_image(self):
        matches = "![alt](https://example.com/img.png) and [link](https://example.com)"
        self.assertListEqual(
            [("alt", "https://example.com/img.png")],
            extract_markdown_images(matches),
        )

    def test_extract_markdown_links_no_anchor(self):
        matches = extract_markdown_links("[](https://example.com)")
        self.assertListEqual([("", "https://example.com")], matches)

if __name__ == "__main__":
    unittest.main()
