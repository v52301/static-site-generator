import unittest

from textnode import TextNode, TextType, split_nodes_link, split_nodes_image, split_nodes_delimiter, extract_markdown_links, extract_markdown_images

class TestSplitNodesImageAndLink(unittest.TestCase):

    def test_split_image_single(self):
        node = TextNode(
            "Here is an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) in text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Here is an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                TextNode(" in text", TextType.TEXT),
            ],
            new_nodes
        )

    def test_split_image_multiple(self):
        # 본문 예시: 이미지가 2개 연속으로 나오는 케이스
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
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_image_at_start(self):
        # 엣지 케이스: 문장이 이미지로 바로 시작할 때 (앞부분 빈 문자열 "" 처리 확인)
        node = TextNode("![start](https://boot.dev/pic.png) followed by text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("start", TextType.IMAGE, "https://boot.dev/pic.png"),
                TextNode(" followed by text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_image_at_end(self):
        # 엣지 케이스: 문장이 이미지로 딱 끝날 때 (뒷부분 빈 문자열 "" 처리 확인)
        node = TextNode("Text ends with an ![end](https://boot.dev/pic.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Text ends with an ", TextType.TEXT),
                TextNode("end", TextType.IMAGE, "https://boot.dev/pic.png"),
            ],
            new_nodes,
        )

    def test_split_image_no_images(self):
        # 이미지가 전혀 없는 일반 텍스트는 원본 그대로 보존되는지 확인
        node = TextNode("Just plain text with no images.", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_image_consecutive(self):
        # 엣지 케이스: 이미지와 이미지 사이에 텍스트가 아예 없을 때
        node = TextNode("![first](https://one.png)![second](https://two.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("first", TextType.IMAGE, "https://one.png"),
                TextNode("second", TextType.IMAGE, "https://two.png"),
            ],
            new_nodes,
        )

    # ==========================
    # 2. 링크 분할 테스트
    # ==========================

    def test_split_link_multiple(self):
        # 본문 예시: 링크가 2개 포함된 기본 케이스
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            new_nodes,
        )

    def test_split_link_at_start(self):
        # 문장 시작이 링크인 케이스
        node = TextNode("[Start Link](https://boot.dev) is first", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Start Link", TextType.LINK, "https://boot.dev"),
                TextNode(" is first", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_link_at_end(self):
        # 문장 끝이 링크인 케이스
        node = TextNode("Ends with [End Link](https://boot.dev)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Ends with ", TextType.TEXT),
                TextNode("End Link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )

    def test_split_link_no_links(self):
        # 링크가 없는 경우
        node = TextNode("No links here at all.", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_link_ignores_image(self):
        # 링크 분할 함수는 이미지 마크다운(![alt](url))을 링크로 오인해 쪼개지 않아야 함
        node = TextNode("Look at this ![image](https://boot.dev/img.png)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)


if __name__ == "__main__":
    unittest.main()