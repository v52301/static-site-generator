import unittest  # 파이썬 기본 제공 테스트 도구 상자를 가져옵니다. 없으면 테스트 프레임워크 자체를 쓸 수 없습니다.

from textnode import (
    TextNode,
    TextType,
    text_node_to_html_node
)  # 검사할 부품인 TextNode 클래스와 TextType 열거형을 가져옵니다.


class TestTextNode(unittest.TestCase):
    # unittest.TestCase를 상속받아야 파이썬 검사기가 "아, 이 안에 적힌 함수들이 테스트 규격이구나" 하고 인식합니다.

    def test_eq(self):
        # 1. 속성이 완전히 같은 두 상자(객체)를 만듭니다.
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        # 2. 두 상자의 내용물이 완벽히 일치하는지 저울에 올려 확인합니다. 다르면 즉시 에러(테스트 실패)를 발생시킵니다.
        self.assertEqual(node, node2)

    def test_eq_false(self):
        # 텍스트 내용이 다른 경우: 일치하지 않아야(assertNotEqual) 정상 통과입니다.
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a different text node", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_eq_false2(self):
        # 타입이 다른 경우: 하나는 일반 텍스트, 하나는 굵은 글씨이므로 달라야 정상입니다.
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        # URL 속성이 다른 경우: URL이 누락되거나 다르면 같다고 판정하면 안 됩니다.
        node = TextNode("Link", TextType.LINK, "https://boot.dev")
        node2 = TextNode("Link", TextType.LINK, "https://google.com")
        self.assertNotEqual(node, node2)

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_image(self):
        node = TextNode("Alt text", TextType.IMAGE, "https://example.com/img.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://example.com/img.png", "alt": "Alt text"}
        )

    def test_bold(self):
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")

    def test_link(self):
        node = TextNode("Click here", TextType.LINK, "https://boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click here")
        self.assertEqual(html_node.props, {"href": "https://boot.dev"})

    def test_invalid_type(self):
        node = TextNode("Invalid", "unknown_type")
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)
            
if __name__ == "__main__":
    unittest.main()  # 터미널에서 이 파일을 직접 실행했을 때 모든 테스트 함수를 차례대로 구동시키는 점화 플러그 역할을 합니다.