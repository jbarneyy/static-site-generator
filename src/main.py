from textnode import TextNode, TextType
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode

from blockfuncs import markdown_to_html_node, extract_title

import os
import sys
import shutil


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    
    copy_src_to_dst("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)


def copy_src_to_dst(src: str, dst: str):
    abs_src = os.path.abspath(src)
    abs_dst = None

    if os.path.exists(os.path.abspath(dst)):
        abs_dst = os.path.abspath(dst)
        shutil.rmtree(abs_dst)
        os.mkdir(abs_dst)
    else:
        os.mkdir(os.path.abspath(dst))
        abs_dst = os.path.abspath(dst)

    src_to_dst_helper(abs_src, abs_dst)


def src_to_dst_helper(src: str, dst: str):
    src_list = os.listdir(src)

    for item in src_list:
        item_src_path = os.path.join(src, item)
        item_dst_path = os.path.join(dst, item)

        if os.path.isfile(item_src_path):
            shutil.copy(item_src_path, item_dst_path)

            print(f"Copying file: {item_src_path} ---> {item_dst_path}")
        else:
            os.mkdir(item_dst_path)

            print(f"Creating new dir and recursing: {item_dst_path}")
            src_to_dst_helper(item_src_path, item_dst_path)


def generate_page(from_path: str, template_path: str, dest_path: str, basepath: str):

    abs_from_path = os.path.abspath(from_path)
    abs_template_path = os.path.abspath(template_path)

    if os.path.exists(os.path.abspath(dest_path)):
        abs_dest_path = os.path.abspath(dest_path)
    else:
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        abs_dest_path = os.path.abspath(dest_path)

    print(abs_from_path)
    print(abs_template_path)
    print(abs_dest_path)

    print(f"Generating page from: {abs_from_path} to: {abs_dest_path} using: {abs_template_path}")

    # Read md file at from_path and store contents in variable #
    with open(abs_from_path, "r") as f:
        md_file = f.read()

    # Read template file at template_path and store contents in variable #
    with open(abs_template_path, "r") as f:
        template_file = f.read()

    # Convert the markdown file into HTML string #
    html_string = markdown_to_html_node(md_file).to_html()

    # Use extract_title function to grab title of the page #
    page_title = extract_title(md_file)

    # Replace the {{ Title }} and {{ Content }} placeholders in template.html with HTML and title generated #
    template_file_replaced = template_file.replace("{{ Title }}", page_title)
    template_file_replaced = template_file_replaced.replace("{{ Content }}", html_string)

    template_file_replaced = template_file_replaced.replace('href="/', f'href="{clean_basepath(basepath)}')
    template_file_replaced = template_file_replaced.replace('src="/', f'src="{clean_basepath(basepath)}')

    print(template_file_replaced)

    # Write new full HTML page to a file at dest_path #
    with open(abs_dest_path, "w") as f:
        f.write(template_file_replaced)


# Crawl every entry in content/, for each md file, generate HTML file using template.html, write to public/ in same dir structure #
def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str, basepath: str):

    abs_source_path = os.path.abspath(dir_path_content)
    abs_template_path = os.path.abspath(template_path)

    os.makedirs(os.path.dirname(os.path.abspath(dest_dir_path)), exist_ok=True)
    abs_dir_path = os.path.abspath(dest_dir_path)

    # Crawl every entry in content/ #
    dir_items = os.listdir(abs_source_path)

    for item in dir_items:
        item_src_path = os.path.join(abs_source_path, item)
        item_dst_path = os.path.join(abs_dir_path, item)

        # md file found, convert md to HTML string using markdown_to_html().to_html(), grab title, replace template.html sections #
        # Write to public/ keeping same dir structure found in content/ while replacing .md with .html #
        if os.path.isfile(item_src_path) and os.path.basename(item_src_path) == "index.md":
            generate_page(item_src_path, abs_template_path, item_dst_path.replace("index.md", "index.html"), basepath)

        # Dir found, call generate_pages_recursive() on sub directory to find more index.md files #
        else:
            generate_pages_recursive(item_src_path, abs_template_path, item_dst_path, basepath)


def clean_basepath(basepath: str):
    if not basepath.startswith("/"):
        basepath = "/" + basepath

    if not basepath.endswith("/"):
        basepath += "/"

    return basepath


main()