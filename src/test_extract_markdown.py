import unittest
from textnode import extract_markdown_images, extract_markdown_links


class TestMarkdownExtraction(unittest.TestCase):
    # ----------------------------------------------------
    # 1. 이미지 추출 테스트 (extract_markdown_images)
    # ----------------------------------------------------
    def test_extract_markdown_images_single(self):
        """단일 이미지가 정상적으로 추출되는지 테스트"""
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        expected = [("image", "https://i.imgur.com/zjjcJKZ.png")]
        self.assertListEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_images_multiple(self):
        """본문에 여러 개의 이미지가 연속/분산되어 있을 때 모두 추출되는지 테스트"""
        text = (
            "Here is ![first](https://example.com/1.png) and "
            "another ![second](https://example.com/2.jpg)"
        )
        expected = [
            ("first", "https://example.com/1.png"),
            ("second", "https://example.com/2.jpg"),
        ]
        self.assertListEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_images_empty_alt(self):
        """alt 텍스트가 비어 있는 경우(![](url)) 빈 문자열로 정상 처리되는지 테스트"""
        text = "Image without alt: ![](https://example.com/empty_alt.png)"
        expected = [("", "https://example.com/empty_alt.png")]
        self.assertListEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_images_no_match(self):
        """이미지가 없는 일반 텍스트일 때 빈 리스트를 반환하는지 테스트"""
        text = "Just normal text without any images or links."
        self.assertListEqual(extract_markdown_images(text), [])

    def test_extract_markdown_images_ignores_regular_links(self):
        """느낌표(!)가 없는 일반 링크는 이미지로 추출하지 않는지 테스트"""
        text = "This is a [link](https://boot.dev), not an image!"
        self.assertListEqual(extract_markdown_images(text), [])

    # ----------------------------------------------------
    # 2. 링크 추출 테스트 (extract_markdown_links)
    # ----------------------------------------------------
    def test_extract_markdown_links_single(self):
        """단일 일반 링크가 정상적으로 추출되는지 테스트"""
        text = "This is text with a link [to boot dev](https://www.boot.dev)"
        expected = [("to boot dev", "https://www.boot.dev")]
        self.assertListEqual(extract_markdown_links(text), expected)

    def test_extract_markdown_links_multiple(self):
        """여러 일반 링크가 본문에 있을 때 순서대로 모두 추출되는지 테스트"""
        text = (
            "Check [Boot.dev](https://www.boot.dev) and "
            "[YouTube](https://www.youtube.com/@bootdotdev)"
        )
        expected = [
            ("Boot.dev", "https://www.boot.dev"),
            ("YouTube", "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertListEqual(extract_markdown_links(text), expected)

    def test_extract_markdown_links_empty_anchor(self):
        """앵커 텍스트가 비어 있는 링크([](url))도 정상 추출되는지 테스트"""
        text = "Empty link text: [](https://empty.example.com)"
        expected = [("", "https://empty.example.com")]
        self.assertListEqual(extract_markdown_links(text), expected)

    def test_extract_markdown_links_no_match(self):
        """링크가 전혀 없는 텍스트일 때 빈 리스트를 반환하는지 테스트"""
        text = "Plain text only."
        self.assertListEqual(extract_markdown_links(text), [])

    def test_extract_markdown_links_ignores_images(self):
        """이미지 문법(![...](...))을 일반 링크로 잘못 인식하지 않는지 검증 (핵심 케이스)"""
        text = "Look at this image ![cute cat](https://example.com/cat.jpg) right here."
        self.assertListEqual(extract_markdown_links(text), [])

    def test_mixed_images_and_links(self):
        """이미지와 링크가 한 문장에 섞여 있을 때 각각 분리되어 정확히 추출되는지 테스트"""
        text = (
            "Click [here](https://boot.dev) to see "
            "![banner](https://boot.dev/banner.png)"
        )
        images = extract_markdown_images(text)
        links = extract_markdown_links(text)

        self.assertListEqual(images, [("banner", "https://boot.dev/banner.png")])
        self.assertListEqual(links, [("here", "https://boot.dev")])


if __name__ == "__main__":
    unittest.main()