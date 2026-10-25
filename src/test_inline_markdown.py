import unittest

from textnode import TextNode, TextType, split_nodes_delimiter

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_delim_code(self):

        node = TextNode("This is text with a 'code block' word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "'", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT)
            ],
            new_nodes
        )

    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT)
            ],
            new_nodes
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT)
            ],
            new_nodes
        )

    def test_delim_bold_and_italic(self):
        # 4. 여러 구분 기호를 연속(체이닝)으로 분할하는 테스트
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_bold_multiple(self):
        # 5. 한 문장에 동일한 구분 기호가 2쌍 이상 있는 경우
        node = TextNode("This has **two** bold **words** here", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This has ", TextType.TEXT),
                TextNode("two", TextType.BOLD),
                TextNode(" bold ", TextType.TEXT),
                TextNode("words", TextType.BOLD),
                TextNode(" here", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_start_and_end(self):
        # 6. 문장의 맨 앞과 맨 끝이 구분 기호인 경우 (빈 문자열이 생기지 않는지 확인)
        node = TextNode("`code at start` and `code at end`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("code at start", TextType.CODE),
                TextNode(" and ", TextType.TEXT),
                TextNode("code at end", TextType.CODE),
            ],
            new_nodes,
        )

    def test_non_text_nodes_preserved(self):
        # 7. 이미 스타일이 적용된 노드(TextType.TEXT가 아닌 노드)는 건드리지 않고 그대로 유지하는지 확인
        nodes = [
            TextNode("already bold", TextType.BOLD),
            TextNode("plain with `code`", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("already bold", TextType.BOLD),
                TextNode("plain with ", TextType.TEXT),
                TextNode("code", TextType.CODE),
            ],
            new_nodes,
        )

    def test_exception_missing_closing_delimiter(self):
        # 8. 닫는 기호가 누락되었을 때 ValueError 예외가 발생하는지 확인
        node = TextNode("This is broken `code block without closing", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

if __name__ == "__main__":
    unittest.main()