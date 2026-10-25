import unittest

from textnode import BlockType, block_to_block_type

class TestBlockToBlockType(unittest.TestCase):
    def test_heading_valid(self):
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)

    def test_heading_invalid(self):
        # # 뒤에 공백이 없는 경우 일반 문단으로 처리
        self.assertEqual(block_to_block_type("#Heading"), BlockType.PARAGRAPH)
        # # 이 7개 이상인 경우 일반 문단으로 처리
        self.assertEqual(block_to_block_type("####### Heading 7"), BlockType.PARAGRAPH)

    # 2. Code Block 테스트
    def test_code_block_valid(self):
        block = "```\ncode line 1\ncode line 2\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_block_invalid(self):
        # 줄바꿈(\n) 없이 붙어있거나 닫는 백틱이 부족한 경우
        self.assertEqual(block_to_block_type("```code```"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("```\ncode line\n``"), BlockType.PARAGRAPH)

    # 3. Quote 테스트
    def test_quote_block_valid(self):
        # 공백이 있는 경우와 없는 경우 모두 허용
        block = "> Quote line 1\n>Quote line 2\n> Quote line 3"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_block_invalid(self):
        # 한 줄이라도 > 로 시작하지 않으면 일반 문단
        block = "> Quote line 1\nQuote line 2 without greater than"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # 4. Unordered List 테스트
    def test_unordered_list_valid(self):
        block = "- item 1\n- item 2\n- item 3"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_invalid(self):
        # '-' 뒤에 공백이 없는 경우
        block = "-item 1\n-item 2"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        # 중간에 '-' 형식이 아닌 줄이 섞인 경우
        block = "- item 1\nitem 2 without dash"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # 5. Ordered List 테스트
    def test_ordered_list_valid(self):
        block = "1. First\n2. Second\n3. Third"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_invalid_start_number(self):
        # 1번부터 시작하지 않은 경우
        block = "2. First\n3. Second"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_invalid_increment(self):
        # 번호가 1씩 증가하지 않고 건너뛴 경우
        block = "1. First\n3. Second"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_missing_space(self):
        # 마침표 뒤에 공백이 없는 경우
        block = "1.First\n2.Second"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # 6. Paragraph (일반 문단) 테스트
    def test_paragraph(self):
        block = "This is just a normal paragraph with some text."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()