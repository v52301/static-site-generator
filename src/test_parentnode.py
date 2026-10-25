import unittest

from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_multiple_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_many_nested_parents(self):
        leaf = LeafNode("b", "deep text")
        level2 = ParentNode("i", [leaf])
        level1 = ParentNode("span", [level2])
        root = ParentNode("div", [level1])
        self.assertEqual(
            root.to_html(),
            "<div><span><i><b>deep text</b></i></span></div>",
        )

    def test_to_html_with_props(self):
        child = LeafNode("p", "paragraph")
        parent = ParentNode(
            "div",
            [child],
            props={"class": "container", "id": "main"},
        )
        self.assertEqual(
            parent.to_html(),
            '<div class="container" id="main"><p>paragraph</p></div>',
        )

    def test_to_html_without_tag_raises_error(self):
        child = LeafNode("span", "text")
        node = ParentNode(None, [child])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_without_children_raises_error(self):
        node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_empty_children_list(self):
        node = ParentNode("div", [])
        self.assertEqual(node.to_html(), "<div></div>")

if __name__ == "__main__":
    unittest.main()