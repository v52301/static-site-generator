from parentnode import ParentNode
from enum import Enum
from leafnode import LeafNode
from pathlib import Path
import re
import os

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)

    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)

    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)

    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)

    if text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})

    if text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})

    raise ValueError(f"Invalid text type: {text_node.text_type}")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        sections = old_node.text.split(delimiter)

        if len(sections) % 2 == 0:
            raise ValueError(f"Invalid markdown syntax: formatted section not closed with '{delimiter}")


        for i in range(len(sections)):
            if sections[i] == "":
                continue

            if i % 2 == 0:
                new_nodes.append(TextNode(sections[i], TextType.TEXT))

            else:
                new_nodes.append(TextNode(sections[i], text_type))

    return new_nodes

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"

    return re.findall(pattern, text)

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"

    return re.findall(pattern, text)

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        original_text = old_node.text
        images = extract_markdown_images(original_text)

        if len(images) == 0:
            new_nodes.append(old_node)
            continue

        for image_alt, image_link in images:
            markdown_image = f"![{image_alt}]({image_link})"
            sections = original_text.split(markdown_image, 1)

            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")

            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))

            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))

            original_text = sections[1]

        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        original_text = old_node.text

        links = extract_markdown_links(original_text)

        if len(links) == 0:
            new_nodes.append(old_node)
            continue

        for link_text, link_url in links:
            markdown_link = f"[{link_text}]({link_url})"

            sections = original_text.split(markdown_link, 1)

            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")

            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))

            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))

            original_text = sections[1]

        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))

    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]

    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)

    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)

    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    nodes = split_nodes_image(nodes)

    nodes = split_nodes_link(nodes)

    return nodes

def markdown_to_blocks(markdown):
    raw_blocks = markdown.split("\n\n")

    blocks = []

    for block in raw_blocks:
        cleaned_block = block.strip()

        if cleaned_block != "":
            blocks.append(cleaned_block)

    return blocks

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block: str) -> BlockType:
    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING

    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE

    lines = block.split("\n")

    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    is_ordered = True

    for i, line in enumerate(lines, start = 1):
        expected_prefix = f"{i}. "
        if not line.startswith(expected_prefix):
            is_ordered = False
            break

    if is_ordered and len(lines) > 0:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)

    return ParentNode("div", children, None)

def block_to_html_node(block):

    block_type = block_to_block_type(block)

    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    
    if block_type == BlockType.CODE:
        return code_to_html_node(block)

    if block_type == BlockType.ORDERED_LIST:
        return olist_to_html_node(block)

    if block_type == BlockType.UNORDERED_LIST:
        return ulist_to_html_node(block)

    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("유효아지 않은 블록 유형입니다.")

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []

    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def paragraph_to_html_node(block):
    # 줄바꿈 문자로 쪼개진 문장들을 공백 하나로 이어 붙여 자연스러운 문단 글자로 만듭니다.
    lines = block.split("\n")
    paragraph = " ".join(lines)
    # 문단 내부의 강조 글자들을 파싱해 자식 요소로 넣고 <p> 태그 상자로 감쌉니다.
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    # 앞에 붙은 '#' 기호의 개수를 세어 h1~h6 태그 레벨을 결정합니다.
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"유효하지 않은 헤딩 레벨: {level}")
    # '# ' 접두사를 제거한 순수 텍스트만 추출합니다.
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    # 맨 앞과 맨 뒤의 ``` 펜스를 제거해 순수 코드 내용만 남깁니다.
    # 코드는 내부의 *나 _가 볼드/기울임꼴로 해석되면 안 되므로 text_to_children을 쓰지 않습니다.
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    # HTML 표준에 따라 <pre> 안에 <code> 태그가 들어가는 이중 구조로 포장합니다.
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    # 줄 단위로 쪼개어 각 번호 매기기 항목을 <li>로 감싸고, 전체를 <ol>로 묶습니다.
    items = block.split("\n")
    html_items = []
    for item in items:
        # '1. ' 같은 앞쪽 숫자와 점, 공백 접두사를 잘라냅니다.
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    # 줄 단위로 쪼개어 글머리 기호 항목을 <li>로 감싸고, 전체를 <ul>로 묶습니다.
    items = block.split("\n")
    html_items = []
    for item in items:
        # '- ' 또는 '* ' 접두사 2글자를 잘라냅니다.
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    # 인용문의 각 줄 앞머리에 붙은 '> ' 또는 '>' 기호를 떼어냅니다.
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("인용 블록 형식이 올바르지 않습니다.")
        new_lines.append(line.lstrip(">").strip())
    # 떼어낸 텍스트들을 공백으로 연결하여 <blockquote> 태그 상자에 넣습니다.
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()

    raise Exception("h1 header not found in markdown")

def generate_page(from_path, template_path, dest_path, basepath= "/"):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    # 1. 마크다운 원본 읽기
    with open(from_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    # 2. 템플릿 HTML 틀 읽기
    with open(template_path, "r", encoding="utf-8") as f:
        template_content = f.read()

    # 3. 마크다운을 HTML 노드 트리로 파싱한 뒤 완성된 HTML 태그 문자열로 직렬화
    node = markdown_to_html_node(md_content)
    html_content = node.to_html()

    # 4. 제목 추출
    title = extract_title(md_content)

    # 5. 템플릿 구멍 메우기 (치환)
    full_html = template_content.replace("{{ Title }}", title)
    full_html = full_html.replace("{{ Content }}", html_content)
    full_html = full_html.replace('href="/', f'href="{basepath}')
    full_html = full_html.replace('src="/', f'src="{basepath}')
    

    # 6. 저장할 대상 폴더가 없으면 미리 생성 (없으면 FileNotFoundError 발생)
    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)

    # 7. 완성된 최종 파일 기록
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(full_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath="/"):

    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)

        if os.path.isfile(from_path):
            if filename.endswith(".md"):
                dest_html_path = Path(dest_path).with_suffix(".html")
                os.makedirs(os.path.dirname(dest_html_path), exist_ok=True)
                generate_page(from_path, template_path, str(dest_html_path), basepath)

        else:
            generate_pages_recursive(from_path, template_path, dest_path, basepath)