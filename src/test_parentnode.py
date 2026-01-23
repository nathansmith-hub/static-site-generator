import unittest

from htmlnode import ParentNode, LeafNode

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
