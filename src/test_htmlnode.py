import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

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

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Hello, world!")
        self.assertEqual(node.to_html(), "<a>Hello, world!</a>")

    def test_leaf_to_html_b(self):
        node = LeafNode("b", "Hello, world!")
        self.assertEqual(node.to_html(), "<b>Hello, world!</b>")

    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "Hello, world!")
        self.assertEqual(node.to_html(), "<h1>Hello, world!</h1>")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_props(self):
        node = LeafNode(
            tag="a",
            value="Google",
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com" target="_blank">Google</a>',
        )

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, World!")
        self.assertEqual(node.to_html(), "Hello, World!")

    def test_leaf_to_html_no_value(self):
        node = LeafNode("a", None)
        with self.assertRaises(ValueError):
            node.to_html()

class TestParentNode(unittest.TestCase):
    def test_parent_to_html_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_parent_to_html_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_parent_to_html_empty_children_list(self):
        parent_node = ParentNode("a", [])
        self.assertEqual(parent_node.to_html(), "<a></a>")

    def test_parent_to_html_child_no_tag(self):
        child_node = LeafNode(None, "no tag")
        parent_node = ParentNode("a", [child_node])
        self.assertEqual(parent_node.to_html(), "<a>no tag</a>")

    def test_parent_to_html_parent_props(self):
        child_node = LeafNode("a", "child")
        parent_node = ParentNode(
            tag="b",
            children=[child_node],
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )
        self.assertEqual(
            parent_node.to_html(),
            '<b href="https://www.google.com" target="_blank"><a>child</a></b>',
        )

    def test_parent_to_html_child_props(self):
        child_node = LeafNode(
            "a",
            "child",
            {
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )
        parent_node = ParentNode("b", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            '<b><a href="https://www.google.com" target="_blank">child</a></b>',
        )
    
    def test_parent_to_html_parent_no_children(self):
        parent_node = ParentNode("p", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_parent_to_html_parent_no_tag(self):
        child_node = LeafNode("a", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_parent_to_html_parent_empty_props(self):
        child_node = LeafNode("a", "child")
        parent_node = ParentNode("p", [child_node], props={})
        self.assertEqual(parent_node.to_html(), "<p><a>child</a></p>")

    def test_parent_to_html_nested_parents_with_props(self):
        grandchild_node = LeafNode("i", "deep")
        child_node = ParentNode("span", [grandchild_node], props={"class": "inner"})
        parent_node = ParentNode("div", [child_node], props={"id": "outer"})
        self.assertEqual(
            parent_node.to_html(),
            '<div id="outer"><span class="inner"><i>deep</i></span></div>',
        )

if __name__ == "__main__":
    unittest.main()
      