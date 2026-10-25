from textnode import TextNode, TextType, generate_pages_recursive
import os
import shutil
import sys

def copy_files_recursive(source_dir, dest_dir):
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)

    for item in os.listdir(source_dir):
        from_path = os.path.join(source_dir, item)
        to_path = os.path.join(dest_dir, item)

        if os.path.isfile(from_path):
            print(f"파일 복사중: {from_path} -> {to_path}")
            shutil.copy(from_path, to_path)

        else:
            print(f"디렉토리 생성 및 진입: {to_path}")
            os.mkdir(to_path)
            copy_files_recursive(from_path, to_path)

def main():

    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    print(f"Generating site with basepath: {basepath}")


    source_dir = "./static"
    destination_dir = "./docs"

    if os.path.exists(destination_dir):
        print(f"기존 {destination_dir} 폴더를 삭제합니다...")
        shutil.rmtree(destination_dir)

    print(f"{source_dir}에서 {destination_dir}로 복사를 시작합니다...")
    copy_files_recursive(source_dir, destination_dir)
    
    node = TextNode("this is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(node)

    # 기존 정적 파일 복사 로직 실행 후...
    generate_pages_recursive("content", "template.html", "docs", basepath)


if __name__ == "__main__":
    main()
