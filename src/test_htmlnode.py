import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_basic(self):
        node = HTMLNode(
            tag="a",
            value="Google",
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )
        self.assertEqual(
            node.props_to_html(),
            ' href="https://www.google.com" target="_blank"',
        )

    def test_props_to_html_none(self):
        node = HTMLNode(tag="p", value="hello", props=None)
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_empty(self):
        node = HTMLNode(tag="p", value="hello", props={})
        self.assertEqual(node.props_to_html(), "")

    def test_repr_includes_fields(self):
        node = HTMLNode(tag="a", value="Link", props={"href": "https://example.com"})
        rep = repr(node)
        self.assertIn("HTMLNode", rep)
        self.assertIn("a", rep)
        self.assertIn("Link", rep)
        self.assertIn("https://example.com", rep)

    def test_constructor_assigns_fields(self):
        children = [HTMLNode(value="child")]
        props = {"class": "btn"}
        node = HTMLNode(tag="button", value="Click", children=children, props=props)
        self.assertEqual(node.tag, "button")
        self.assertEqual(node.value, "Click")
        self.assertEqual(node.children, children)
        self.assertEqual(node.props, props)

if __name__ == "__main__":
    unittest.main()
      