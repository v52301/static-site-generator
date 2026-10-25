import unittest
from textnode import markdown_to_blocks

class TestMarkDownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):

        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""

        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ]
        )

    def test_markdown_to_blocks_excess_newlines(self):
        # 2. 빈 줄이 3개 이상 과도하게 연속으로 들어갔을 때 빈 블록이 생기지 않는지 검증
        md = """
# Heading 1




Paragraph after multiple newlines


- List item
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Heading 1",
                "Paragraph after multiple newlines",
                "- List item",
            ],
        )

    def test_markdown_to_blocks_leading_trailing_spaces(self):
        # 3. 각 블록 앞뒤에 스페이스나 줄바꿈이 지저분하게 붙어있을 때 strip이 잘 되는지 검증
        md = """
   This block has leading whitespace   

   This block has trailing whitespace   
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This block has leading whitespace",
                "This block has trailing whitespace",
            ],
        )

    def test_markdown_to_blocks_single_block(self):
        # 4. 빈 줄 없이 단일 블록만 입력되었을 때
        md = "Just a single paragraph without any extra blocks."
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Just a single paragraph without any extra blocks.",
            ],
        )

    def test_markdown_to_blocks_empty(self):
        # 5. 빈 문자열이나 공백/줄바꿈만 들어왔을 때 빈 리스트를 반환하는지 검증
        md = "   \n\n   \n\n   "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])


if __name__ == "__main__":
    unittest.main()